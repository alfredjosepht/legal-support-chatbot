#!/usr/bin/env python3
"""Integration tests for cyberbullying and physical assault classification."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import spacy
from nlp.postprocess import postprocess_categories

nlp = spacy.load(str(PROJECT_ROOT / "models" / "legal_textcat"))

samples = [
    ("Someone is insulting me on Instagram and posting my photos to humiliate me", "cyber_bullying"),
    ("My classmate shoved me in the corridor", "physical_assault"),
    ("They keep sending me abusive messages online every day", "cyber_bullying"),
    ("A person threatened to post my private photos online if I don't pay", None),  # could be threats or cyber_bullying
    ("Someone stole my phone and beat me", "physical_assault"),
    ("People are saying false things about me on WhatsApp groups", "cyber_bullying"),
    ("I was pushed and injured during a fight", "physical_assault"),
    ("Anonymous accounts keep sending me nasty comments on social media", "cyber_bullying"),
    ("he bullied me", "cyber_bullying"),
    ("they are bullying me", "cyber_bullying"),
]

passed = 0
failed = 0

for text, expected_primary in samples:
    doc = nlp(text)
    raw_cats = doc.cats
    final_cats, context = postprocess_categories(text, raw_cats)
    
    primary = max(final_cats, key=final_cats.get) if final_cats else "unknown"
    
    print(f"\nINPUT: {text}")
    print(f"Context: {context}")
    top5 = {k: round(v, 3) for k, v in sorted(raw_cats.items(), key=lambda x: x[1], reverse=True)[:5]}
    print(f"Raw cats (top 5): {top5}")
    print(f"Final cats: {final_cats}")
    
    if expected_primary is not None:
        if expected_primary in final_cats:
            print(f"[PASS] '{expected_primary}' found in final_cats")
            passed += 1
        else:
            print(f"[FAIL] Expected '{expected_primary}' in final_cats, got: {list(final_cats.keys())}")
            failed += 1
    else:
        print(f"[SKIP] No assertion for this sample (primary={primary})")
        passed += 1

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    sys.exit(1)
