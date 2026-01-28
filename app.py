from fastapi import FastAPI
import spacy
import json
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

CONFIDENCE_THRESHOLD = 0.1
app = FastAPI(title="Legal Support Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


nlp = spacy.load("models/legal_textcat")

with open("data/law_mapping.json", encoding="utf-8") as f:
    law_mapping = json.load(f)

with open("data/legal_steps.json", encoding="utf-8") as f:
    legal_steps = json.load(f)

with open("data/resources.json", encoding="utf-8") as f:
    resources = json.load(f)

with open("data/case_laws.json", encoding="utf-8") as f:
    case_laws = json.load(f)


@app.get("/")
def root():
    return {"status": "Backend running"}

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    category: str                  # primary
    confidence: float
    reason: str
    matched_categories: list       # 👈 NEW
    laws: list
    steps: list
    resources: list
    case_references: list



@app.post("/chat", response_model=ChatResponse)
def chat(user_input: ChatRequest):

    text = user_input.message.strip()

    if not text:
        return {
            "category": "unknown",
            "confidence": 0.0,
            "reason": "empty_input",
            "matched_categories": [],
            "laws": [],
            "steps": [],
            "resources": [],
            "case_references": []
        }

    doc = nlp(text)

    matched_categories = []

    if doc.cats:
        matched_categories = [
            {
                "category": k,
                "confidence": round(float(v), 3)
            }
            for k, v in doc.cats.items()
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
    raw_laws = law_mapping.get(category, {})
    raw_steps = legal_steps.get(category, {})
    raw_resources = resources.get(category, {})


    return {
        "category": category,
        "confidence": confidence,
        "reason": reason,
        "matched_categories": matched_categories,

    # ✅ FIXED: always lists
        "laws": (
            raw_laws.get("laws", [])
            if isinstance(raw_laws, dict)
            else raw_laws
        ),

        "steps": (
           raw_steps.get("common_situations", [])
           + raw_steps.get("how_people_commonly_proceed", [])
           + raw_steps.get("precautions", [])
           if isinstance(raw_steps, dict)
           else raw_steps
        ),

        "resources": (
            raw_resources.get("police_stations", [])
            + raw_resources.get("helplines", [])
            + raw_resources.get("legal_aid", [])
            if isinstance(raw_resources, dict)
            else raw_resources
        ),

        "case_references": case_laws.get(category, [])
}

