#!/usr/bin/env python3
"""Integration tests for query classification."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import spacy
from nlp.postprocess import postprocess_categories

nlp = spacy.load(str(PROJECT_ROOT / "models" / "legal_textcat"))

samples = [
    ("Someone is insulting me on Instagram and posting my photos to humiliate me", ["cyber_bullying","cyber_harassment"]),
    ("My classmate shoved me in the corridor", "physical_assault"),
    ("They keep sending me abusive messages online every day", ["cyber_bullying","cyber_harassment"]),
    ("A person threatened to post my private photos online if I don't pay",["blackmail_extortion","cyber_sexual_crime","threats"]),  # could be threats or cyber_bullying
    ("Someone stole my phone and beat me", "physical_assault"),
    ("People are saying false things about me on WhatsApp groups",["cyber_harassment", "defamation_privacy_fraud"]),
    ("I was pushed and injured during a fight", "physical_assault"),
    ("Anonymous accounts keep sending me nasty comments on social media", "cyber_harassment"),
    ("he bullied me", "ragging"),
    ("my senior raped me",["sexual_assault","ragging","physical_assault"]),
    ("my professor touched me","sexual_harassment"),
    ("my professor made sexual comments about me","sexual_harassment"),
    ("someone is stalking me","stalking"),
    ("the college withheld my tc","institutional_misconduct"),
    ("my ex threatens to leak my naked photos", ["cyber_sexual_crime", "threats"]),
    ("someone created a fake id of mine","impersonation_doxxing"),
    ("my friend spread false rumors about me","defamation_privacy_fraud"),
    ("my husband kicked me","physical_assault"),
    ("i think someone is tracking my location","cyber_harassment"),
    ("my professor reduced my internal marks unnecessarly","administrative_violation"),
    ("a stranger took my photo without my permission","defamation_privacy_fraud"),
    ("the didnt allow me in becuase i am a hindu","religious_discrimination"),
    ("they avoided me because i am black","racism"),
    ("they mocked me since i am from a lower caste family","caste_discrimination"),
    ("they call me bad words","verbal_abuse"),
    ("a person is telling lies about me and ruining my name and reputation on facebook",["defamation_privacy_fraud","cyber_harassment"]),
    ("a person is constantly stalking me and sending me messages ",["cyber_harassment","stalking"]),
    ("a person is hating on my community on instagram","online_hate_speech"),
    ("my friends in school are insulting me in my dms",["cyber_bullying","verbal_abuse"]),
    ("she is threatening me that she would leak my chats if i dont pay her",["blackmail_extortion","threats"]),
    ("my boyfriend has my nude photos",["cyber_sexual_crime"])
]

passed = 0
failed = 0

for text, expected in samples:
    doc = nlp(text)
    raw_cats = doc.cats
    final_cats, context = postprocess_categories(text, raw_cats)
    
    primary = max(final_cats, key=final_cats.get) if final_cats else "unknown"
    
    print(f"\nINPUT: {text}")
    print(f"Context: {context}")
    top5 = {k: round(v, 3) for k, v in sorted(raw_cats.items(), key=lambda x: x[1], reverse=True)[:5]}
    print(f"Raw cats (top 5): {top5}")
    print(f"Final cats: {final_cats}")
    
    if expected is not None:
        expected_list = [expected] if isinstance(expected, str) else list(expected)
        missing = [cat for cat in expected_list if cat not in final_cats]
        
        if not missing:
            print(f"[PASS] All expected categories {expected_list} found in final_cats")
            passed += 1
        else:
            print(f"[FAIL] Missing {missing} from final_cats. Expected: {expected_list}, Got: {list(final_cats.keys())}")
            failed += 1
    else:
        print(f"[SKIP] No assertion for this sample (primary={primary})")
        passed += 1

print(f"\n{'='*50}")
print(f"Results: {passed} passed, {failed} failed")
if failed:
    sys.exit(1)
