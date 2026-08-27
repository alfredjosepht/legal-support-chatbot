import spacy
import pandas as pd
from pathlib import Path
from spacy.training.example import Example

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "dataset.csv"
MODEL_OUTPUT = BASE_DIR / "models" / "legal_textcat"

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Create a blank English NLP model
nlp = spacy.blank("en")

# Add text classification pipeline
textcat = nlp.add_pipe("textcat")

# Add labels (categories)
labels = df["label"].unique()
for label in labels:
    textcat.add_label(label)

# Prepare training examples
examples = []
for _, row in df.iterrows():
    doc = nlp.make_doc(row["text"])
    cats = {label: False for label in labels}
    cats[row["label"]] = True
    examples.append(Example.from_dict(doc, {"cats": cats}))

# Train the model
optimizer = nlp.begin_training()

for epoch in range(20):
    losses = {}
    nlp.update(examples, sgd=optimizer, losses=losses)
    print(f"Epoch {epoch + 1} - Loss: {losses}")

# Save the trained model
nlp.to_disk(str(MODEL_OUTPUT))

print(f"Training completed. Model saved in {MODEL_OUTPUT}")
