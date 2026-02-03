#!/usr/bin/env python3
import sys
sys.path.insert(0, "nlp")
import spacy
from postprocess_v2 import postprocess_categories

nlp = spacy.load("models/legal_textcat")

samples = [
    "Someone is insulting me on Instagram and posting my photos to humiliate me",
    "My classmate shoved me in the corridor",
    "They keep sending me abusive messages online every day",
    "A person threatened to post my private photos online if I don't pay",
    "Someone stole my phone and beat me",
    "People are saying false things about me on WhatsApp groups",
    "I was pushed and injured during a fight",
    "Anonymous accounts keep sending me nasty comments on social media",
]

for text in samples:
    doc = nlp(text)
    raw_cats = doc.cats
    final_cats, context = postprocess_categories(text, raw_cats)
    print("\nINPUT:", text)
    print("Context:", context)
    print("Raw cats (top 5):", {k: round(v,3) for k,v in sorted(raw_cats.items(), key=lambda x: x[1], reverse=True)[:5]})
    print("Final cats:", final_cats)
