"""Inference helper for binary complaint detection using Logistic Regression + TF-IDF."""

import os
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "complaint_detector"
MODEL_PATH = MODEL_DIR / "logreg_model.joblib"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"

_model = None
_vectorizer = None


def load_detector_artifacts():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
            # Lazy train if model files don't exist yet
            from nlp.train_complaint_detector import train_complaint_detector
            train_complaint_detector()
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VECTORIZER_PATH)
    return _model, _vectorizer


def predict_complaint(text: str) -> dict:
    """Classify input text as 'complaint' or 'not_complaint'.

    Returns a dict with:
    - label: 'complaint' or 'not_complaint'
    - confidence: float between 0.0 and 1.0
    - probabilities: dict of class probabilities
    - is_complaint: boolean (True if complaint, False if not_complaint)
    """
    cleaned_text = (text or "").strip()
    if not cleaned_text:
        return {
            "label": "not_complaint",
            "confidence": 1.0,
            "probabilities": {
                "complaint": 0.0,
                "not_complaint": 1.0
            },
            "is_complaint": False
        }

    model, vectorizer = load_detector_artifacts()
    
    vec = vectorizer.transform([cleaned_text])
    pred_label = str(model.predict(vec)[0])
    probs = model.predict_proba(vec)[0]
    
    prob_dict = {}
    for idx, cls_name in enumerate(model.classes_):
        prob_dict[str(cls_name)] = float(f"{probs[idx]:.4f}")
    
    confidence = float(f"{max(probs):.4f}")
    
    return {
        "label": pred_label,
        "confidence": confidence,
        "probabilities": prob_dict,
        "is_complaint": (pred_label == "complaint")
    }
