"""Train a binary Logistic Regression + TF-IDF classifier to detect whether input is a complaint or not_complaint."""

import os
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "complaint_dataset.csv"
MODEL_DIR = BASE_DIR / "models" / "complaint_detector"
MODEL_PATH = MODEL_DIR / "logreg_model.joblib"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.joblib"


def train_complaint_detector():
    print(f"Loading binary dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    
    X = df["text"].astype(str)
    y = df["label"].astype(str)
    
    print(f"Total samples: {len(df)}")
    print(f"Class breakdown:\n{y.value_counts()}\n")
    
    # Stratified Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)} | Test samples: {len(X_test)}")
    
    # TF-IDF Feature Extraction
    print("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
        sublinear_tf=True,
        strip_accents="unicode",
        lowercase=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train Logistic Regression Classifier
    print("Training Logistic Regression Classifier...")
    model = LogisticRegression(
        class_weight="balanced",
        C=2.0,
        max_iter=1000,
        random_state=42,
        solver="lbfgs"
    )
    model.fit(X_train_vec, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_vec)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "=" * 50)
    print(f"Evaluation Metrics on Test Set (Accuracy: {accuracy:.4f}):")
    print("=" * 50)
    print(classification_report(y_test, y_pred, digits=4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Save artifacts
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"\nModel artifacts saved successfully:")
    print(f"  - Model:      {MODEL_PATH}")
    print(f"  - Vectorizer: {VECTORIZER_PATH}")
    
    # Quick sanity check predictions
    test_queries = [
        "hello",
        "good morning",
        "thanks for the help",
        "what is the time",
        "tell me a joke",
        "my senior punched me",
        "someone leaked my photo",
        "my teacher is harassing me",
        "I am being blackmailed",
        "the college withheld my documents illegally"
    ]
    
    print("\nSanity Check Sample Predictions:")
    for query in test_queries:
        vec = vectorizer.transform([query])
        pred_label = model.predict(vec)[0]
        pred_probs = model.predict_proba(vec)[0]
        classes = list(model.classes_)
        conf = max(pred_probs)
        print(f"  - [{pred_label:14}] (conf: {conf:.2f}) -> \"{query}\"")


if __name__ == "__main__":
    train_complaint_detector()
