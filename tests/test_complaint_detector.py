#!/usr/bin/env python3
"""Unit tests for Logistic Regression + TF-IDF complaint detector."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from nlp.complaint_detector import predict_complaint

def test_complaint_predictions():
    test_cases = [
        # Non-complaints
        ("hello", "not_complaint"),
        ("hi judi", "not_complaint"),
        ("good morning", "not_complaint"),
        ("thanks for the help", "not_complaint"),
        ("how are you doing", "not_complaint"),
        ("what is the time", "not_complaint"),
        ("tell me a joke", "not_complaint"),
        ("can you help me with math", "not_complaint"),
        ("bye take care", "not_complaint"),
        ("okay got it", "not_complaint"),
        
        # Complaints
        ("my senior punched me", "complaint"),
        ("someone leaked my photo", "complaint"),
        ("my teacher is harassing me", "complaint"),
        ("I am being blackmailed with private pictures", "complaint"),
        ("he raped me", "complaint"),
        ("people are discriminating against me because of my caste", "complaint"),
        ("the college is illegally withholding my degree certificate", "complaint"),
        ("they beat me up in the hostel", "complaint"),
        ("someone created a fake profile with my name and phone number", "complaint"),
        ("my professor made inappropriate sexual comments", "complaint"),
    ]
    
    passed = 0
    failed = 0
    
    print("Testing Complaint Detector Gate:")
    print("=" * 60)
    
    for text, expected in test_cases:
        res = predict_complaint(text)
        pred = res["label"]
        conf = res["confidence"]
        status = "[PASS]" if pred == expected else "[FAIL]"
        if pred == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} | Pred: {pred:14} (conf: {conf:.2f}) | Expected: {expected:14} | Text: \"{text}\"")
        
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    assert failed == 0, f"{failed} test cases failed!"

if __name__ == "__main__":
    test_complaint_predictions()
    print("\n[ALL PASS] Complaint detector unit tests passed successfully!")
