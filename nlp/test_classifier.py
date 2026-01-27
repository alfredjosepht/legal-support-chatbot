import spacy
from postprocess import postprocess_categories

nlp = spacy.load("models/legal_textcat")

while True:
    text = input("Enter a student problem (or type exit): ")
    if text.lower() == "exit":
        break

    doc = nlp(text)

    final_labels = postprocess_categories(text, doc.cats)

    if not final_labels:
        print("⚠️ Unable to clearly classify. Please provide more details.")
    else:
        print("\nRelevant issue categories:")
        for label, score in final_labels.items():
            print(f"- {label} ({score:.2f})")

    print("-" * 40)

