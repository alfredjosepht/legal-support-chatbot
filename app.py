from fastapi import FastAPI, HTTPException
import hashlib
import secrets
import os
import spacy
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
sys.path.insert(0, "nlp")
from postprocess_v2 import postprocess_categories, get_legal_framework

# Updated with complete law mappings for all 20 crime types
CONFIDENCE_THRESHOLD = 0.05  # Lowered to catch all crime types with improved training data. Model retrained.
app = FastAPI(title="Legal Support Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


nlp = spacy.load("models/legal_textcat")

with open("data/law_mapping_enhanced.json", encoding="utf-8") as f:
    law_mapping = json.load(f)


with open("data/resources.json", encoding="utf-8") as f:
    resources = json.load(f)

with open("data/case_laws.json", encoding="utf-8") as f:
    case_laws = json.load(f)


@app.get("/")
def root():
    return {"status": "Backend running"}

class ChatRequest(BaseModel):
    message: str


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


@app.post('/consultations/{username}')
def save_consultations(username: str, payload: ConsultationsPayload):
    p = consultations_path_for(username)
    try:
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({"consultations": [c.dict() for c in payload.consultations], "activeConsultationId": payload.activeConsultationId}, f, indent=2, ensure_ascii=False)
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
            "matched_categories": [],
            "context": {},
            "legal_frameworks": [],
            "laws": [],
            "steps": [],
            "resources": [],
            "case_references": [],
            "warnings": []
        }

    doc = nlp(text)

    # Apply postprocessing with context extraction and age-based rules
    final_cats, context = postprocess_categories(text, doc.cats)

    matched_categories = []
    warnings = []

    if final_cats:
        matched_categories = [
            {
                "category": k,
                "confidence": round(float(v), 3)
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
    
    # Get legal frameworks
    legal_frameworks = get_legal_framework(category, context)
    
    # Get comprehensive laws from enhanced mapping
    raw_laws = law_mapping.get(category, {})
    laws_to_return = raw_laws.get("laws", []) if isinstance(raw_laws, dict) else []
    
    # Get procedural steps (filing_procedure from enhanced mapping)
    procedural_steps = raw_laws.get("filing_procedure", []) if isinstance(raw_laws, dict) else []
    raw_resources = resources.get(category, {})
    
    # Combine procedural steps with general steps

    return {
        "category": category,
        "confidence": confidence,
        "reason": reason,
        "matched_categories": matched_categories,
        "context": {
            "age_indicator": context.get('age_indicator'),
            "authority": context.get('authority'),
            "medium": context.get('medium'),
            "discrimination_types": context.get('discrimination_types', []),
            "legal_framework": context.get('legal_framework')
        },
        "legal_frameworks": legal_frameworks,
        "laws": laws_to_return,
        "steps":procedural_steps,
        "resources": (
            raw_resources.get("police_stations", [])
            + raw_resources.get("helplines", [])
            + raw_resources.get("legal_aid", [])
            if isinstance(raw_resources, dict)
            else raw_resources
        ),
        "case_references": case_laws.get(category, []),
        "warnings": warnings
    }

