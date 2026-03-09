import spacy
from nlp.postprocess_v2 import postprocess_categories

nlp_model = spacy.load("models/legal_textcat")
text = "my classmates insulted me becuase of my caste"
doc = nlp_model(text)

print("Raw Categories:")
for cat, score in sorted(doc.cats.items(), key=lambda x: x[1], reverse=True):
    if score > 0.01:
        print(f"  {cat}: {score:.4f}")

final_cats, contextContext = postprocess_categories(text, doc.cats)
print("\nFinal Categories:")
for cat, score in final_cats.items():
    print(f"  {cat}: {score:.4f}")
