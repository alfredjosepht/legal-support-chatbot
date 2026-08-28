import random
import spacy
import pandas as pd
from pathlib import Path
from spacy.training.example import Example

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "dataset.csv"
MODEL_OUTPUT = BASE_DIR / "models" / "legal_textcat"

random.seed(42)  # reproducible shuffling

# Load dataset
df = pd.read_csv(DATASET_PATH)

# Create a blank English NLP model
nlp = spacy.blank("en")

# Add text classification pipeline (multi-label: independent sigmoid per category)
textcat = nlp.add_pipe("textcat_multilabel")

# Add labels (categories)
labels = df["label"].unique()
for label in labels:
    textcat.add_label(label)

# Prepare training examples
examples = []
for _, row in df.iterrows():
    doc = nlp.make_doc(row["text"])
    cats = {label: 0 for label in labels}
    primary = row["label"]
    cats[primary] = 1
    examples.append(Example.from_dict(doc, {"cats": cats}))

# Train the model
optimizer = nlp.begin_training()

for epoch in range(25):
    random.shuffle(examples)  # reshuffle every epoch
    losses = {}
    nlp.update(examples, sgd=optimizer, losses=losses)
    print(f"Epoch {epoch + 1} - Loss: {losses}")

# Save the trained model
nlp.to_disk(str(MODEL_OUTPUT))

print(f"Training completed. Model saved in {MODEL_OUTPUT}")