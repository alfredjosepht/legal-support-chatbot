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
    category: str
    confidence: float
    reason: str
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
            "laws": [],
            "steps": [],
            "resources": [],
            "case_references": []
        }

    doc = nlp(text)

    # Default safe values
    category = "unknown"
    confidence = 0.0
    reason = "model_not_available"

    if doc.cats:
        category = max(doc.cats, key=doc.cats.get)
        confidence = float(doc.cats[category])
        reason = "low_confidence"

        if confidence >= CONFIDENCE_THRESHOLD:
            reason = "classified"
        else:
            category = "unknown"

    return {
        "category": category,
        "confidence": round(confidence, 3),
        "reason": reason,
        "laws": law_mapping.get(category, []),
        "steps": legal_steps.get(category, []),
        "resources": resources.get(category, []),
        "case_references": case_laws.get(category, [])
    }

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": bool(nlp),
        "confidence_threshold": CONFIDENCE_THRESHOLD
    }

