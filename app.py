from pathlib import Path
from fastapi import FastAPI, HTTPException
import hashlib
import secrets
import os
import spacy
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp.postprocess import postprocess_categories, get_legal_framework
from nlp.complaint_detector import predict_complaint
from nlp.llm_client import generate_legal_summary

BASE_DIR = Path(__file__).resolve().parent

# Updated with complete law mappings for all 20 crime types
CONFIDENCE_THRESHOLD = 0.25  # Balanced threshold for high accuracy
app = FastAPI(title="Legal Support Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


nlp = spacy.load(str(BASE_DIR / "models" / "legal_textcat"))

with open(BASE_DIR / "data" / "law_mapping_enhanced.json", encoding="utf-8") as f:
    law_mapping = json.load(f)

with open(BASE_DIR / "data" / "resources.json", encoding="utf-8") as f:
    resources = json.load(f)

# Local, location-specific contact numbers (overrides / additions for returned resources)
with open(BASE_DIR / "data" / "local_numbers.json", encoding="utf-8") as f:
    local_numbers = json.load(f)

with open(BASE_DIR / "data" / "case_laws.json", encoding="utf-8") as f:
    case_laws = json.load(f)


@app.get("/")
def root():
    return {"status": "Backend running"}

class ChatRequest(BaseModel):
    message: str
    # optional location chosen by frontend (e.g. "Kerala", "Mumbai")
    location: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


def hash_password(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${digest}"


def load_users() -> dict:
    users_file = os.path.join("data", "users.json")
    os.makedirs(os.path.dirname(users_file), exist_ok=True)
    users = {}
    if os.path.exists(users_file):
        try:
            with open(users_file, encoding="utf-8") as f:
                users = json.load(f)
        except Exception:
            users = {}
    return users


def save_users(users: dict):
    users_file = os.path.join("data", "users.json")
    os.makedirs(os.path.dirname(users_file), exist_ok=True)
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def verify_password(stored: str, password: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
    except Exception:
        return False
    check = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return secrets.compare_digest(check, digest)


@app.post('/signup')
def signup(payload: LoginRequest):
    username = payload.username.strip()
    password = payload.password
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="username already exists")

    users[username] = {"password": hash_password(password)}
    save_users(users)
    return {"status": "ok", "user": username}


@app.post('/login')
def login(payload: LoginRequest):
    username = payload.username.strip()
    password = payload.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password required")

    users = load_users()
    entry = users.get(username)
    if not entry:
        raise HTTPException(status_code=401, detail="invalid credentials")

    stored = entry.get('password')
    if not stored or not verify_password(stored, password):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return {"status": "ok", "user": username}


class ChatResponse(BaseModel):
    category: str                  # primary
    confidence: float
    reason: str
    matched_categories: list
    context: dict                  # NEW: age, authority, medium, discrimination types
    legal_frameworks: list         # NEW: applicable legal frameworks
    laws: list
    steps: list
    resources: list
    case_references: list
    warnings: list                 # NEW: safety flags or additional notes
    is_complaint: bool | None = True
    message: str | None = None
    status: str | None = None
    answer_text: str | None = None



class Message(BaseModel):
    id: int
    text: str | None = None
    role: str
    time: str | None = None
    files: list | None = None
    data: dict | None = None


class Consultation(BaseModel):
    id: str
    title: str | None = None
    messages: list[Message] | None = []
    timestamp: str | None = None


class ConsultationsPayload(BaseModel):
    consultations: list[Consultation]
    activeConsultationId: str | None = None


def consultations_path_for(username: str) -> str:
    path = os.path.join('data', 'consultations')
    os.makedirs(path, exist_ok=True)
    return os.path.join(path, f"{username}.json")


@app.get('/consultations/{username}')
def get_consultations(username: str):
    p = consultations_path_for(username)
    if os.path.exists(p):
        try:
            with open(p, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"consultations": [], "activeConsultationId": None}
    return {"consultations": [], "activeConsultationId": None}


@app.get('/locations')
def get_locations():
    """Return available location choices (read from data/local_numbers.json).
    Frontend uses this to populate the location selector."""
    try:
        # include a default 'National' option on the frontend
        return {"locations": ["national"] + sorted(list(local_numbers.keys()))}
    except Exception:
        return {"locations": ["national"]}

@app.post('/consultations/{username}')
def save_consultations(username: str, payload: ConsultationsPayload):
    p = consultations_path_for(username)
    try:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({"consultations": [c.model_dump() for c in payload.consultations], "activeConsultationId": payload.activeConsultationId}, f, indent=2, ensure_ascii=False)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/chat", response_model=ChatResponse)
def chat(user_input: ChatRequest):

    text = user_input.message.strip()

    if not text:
        return {
            "category": "unknown",
            "confidence": 0.0,
            "reason": "empty_input",
            "is_complaint": False,
            "status": "not_complaint",
            "message": "Please describe the legal issue or incident you want help with.",
            "answer_text": "Please describe the legal issue or incident you want help with.",
            "matched_categories": [],
            "context": {},
            "legal_frameworks": [],
            "laws": [],
            "steps": [],
            "resources": [],
            "case_references": [],
            "warnings": []
        }

    location = user_input.location or None

    # Stage 1: Binary Complaint Detection Gate (Logistic Regression + TF-IDF)
    complaint_eval = predict_complaint(text)
    if not complaint_eval.get("is_complaint", False):
        return {
            "category": "not_complaint",
            "confidence": complaint_eval["confidence"],
            "reason": "not_complaint",
            "is_complaint": False,
            "status": "not_complaint",
            "message": "Please describe the legal issue or incident you want help with.",
            "answer_text": "Please describe the legal issue or incident you want help with.",
            "matched_categories": [],
            "context": {
                "age_indicator": None,
                "authority": None,
                "medium": None,
                "discrimination_types": [],
                "legal_framework": None,
                "location": location
            },
            "legal_frameworks": [],
            "laws": [],
            "steps": [],
            "resources": [],
            "case_references": [],
            "warnings": []
        }

    # Stage 2: spaCy Multi-Class Crime Classification & Legal Mapping (Complaints only)
    doc = nlp(text)

    # Apply postprocessing with context extraction and age-based rules
    final_cats, context = postprocess_categories(text, doc.cats)

    matched_categories = []
    warnings = []

    if final_cats:
        matched_categories = [
            {
                "category": k,
                "confidence": float(f"{v:.3f}")
            }
            for k, v in final_cats.items()
            if v >= CONFIDENCE_THRESHOLD
        ]

        matched_categories.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

    if matched_categories:
        primary = matched_categories[0]
        category = primary["category"]
        confidence = primary["confidence"]
        reason = "classified"
    else:
        category = "unknown"
        confidence = 0.0
        reason = "low_confidence"
    
    # Age-based warnings
    if context.get('age_indicator') is None and any(
        keyword in text.lower() for keyword in 
        ['sexual', 'harassment', 'assault', 'abuse', 'touching', 'contact']
    ):
        warnings.append("Age information not provided. For sexual offences, age determines legal framework (POCSO for minors).")
    
    location = user_input.location or None
    loc_contacts = local_numbers.get(location, {}) if location else {}

    # Aggregate legal frameworks, laws, steps, and resources for all matched categories
    all_legal_frameworks = []
    all_laws = []
    all_steps = []
    all_resources = []
    all_case_references = []
    
    cats_to_process = [c["category"] for c in matched_categories] if matched_categories else [category]
    
    seen_frameworks = set()
    seen_laws = set()
    seen_steps = set()
    seen_case_refs = set()
    
    for cat in cats_to_process:
        # Frameworks
        fw_list = get_legal_framework(cat, context)
        for fw in fw_list:
            if fw not in seen_frameworks:
                seen_frameworks.add(fw)
                all_legal_frameworks.append(fw)
        
        # Laws & Steps
        c_raw_laws = law_mapping.get(cat, {})
        c_laws = c_raw_laws.get("laws", []) if isinstance(c_raw_laws, dict) else []
        for law in c_laws:
            law_key = f"{law.get('act', '')}-{law.get('section', '')}"
            if law_key not in seen_laws:
                seen_laws.add(law_key)
                all_laws.append(law)
                
        c_steps = c_raw_laws.get("filing_procedure", []) if isinstance(c_raw_laws, dict) else []
        for step in c_steps:
             if step not in seen_steps:
                 seen_steps.add(step)
                 all_steps.append(step)
                 
        # Resources
        c_resources = resources.get(cat, {})
        if isinstance(c_resources, dict):
            for res_list in [c_resources.get("police_stations"), c_resources.get("helplines"), c_resources.get("legal_aid")]:
                if res_list and isinstance(res_list, list):
                    all_resources.extend(res_list)
            
        # Case References
        c_case_refs = case_laws.get(cat, [])
        if isinstance(c_case_refs, list):
            for ref in c_case_refs:
                ref_id = str(ref) if isinstance(ref, dict) else ref
                if ref_id not in seen_case_refs:
                    seen_case_refs.add(ref_id)
                    all_case_references.append(ref)

    # Add location specific contacts
    if isinstance(loc_contacts, dict):
        for res_list in [loc_contacts.get("police_stations"), loc_contacts.get("helplines"), loc_contacts.get("legal_aid")]:
            if res_list and isinstance(res_list, list):
                all_resources.extend(res_list)

    report_payload = {
        "user_query": text,
        "category": category,
        "confidence": confidence,
        "reason": reason,
        "is_complaint": True,
        "status": "complaint",
        "matched_categories": matched_categories,
        "context": {
            "age_indicator": context.get('age_indicator'),
            "authority": context.get('authority'),
            "medium": context.get('medium'),
            "discrimination_types": context.get('discrimination_types', []),
            "legal_framework": context.get('legal_framework'),
            "location": location
        },
        "legal_frameworks": all_legal_frameworks,
        "laws": all_laws,
        "steps": all_steps,
        "resources": all_resources,
        "case_references": all_case_references,
        "warnings": warnings
    }

    # Stage 3: Local LLM Response Formatting Layer (Ollama + Qwen)
    answer_text = generate_legal_summary(report_payload)
    report_payload["answer_text"] = answer_text

    return report_payload

