"""
Optimized training script using en_core_web_md as a VECTOR SOURCE.
- Large batch sizes (16→128) for fast CPU throughput
- 20 epochs is sufficient given the fast loss convergence with word vectors
"""
import random
import spacy
import pandas as pd
from pathlib import Path
from spacy.training.example import Example
from spacy.util import minibatch, compounding

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "dataset.csv"
MODEL_OUTPUT = BASE_DIR / "models" / "legal_textcat"

random.seed(42)

print("Running on CPU (CUDA Toolkit not installed)")

df = pd.read_csv(DATASET_PATH)
labels = df["label"].unique()

# Load en_core_web_md — only tok2vec + vectors, drop the rest
print("Loading en_core_web_md as vector source...")
nlp = spacy.load(
    "en_core_web_md",
    exclude=["tagger", "parser", "ner", "senter", "attribute_ruler", "lemmatizer"]
)

# Add multilabel text classifier
textcat = nlp.add_pipe("textcat_multilabel")
for label in labels:
    textcat.add_label(label)

# Build training examples
def get_examples():
    for _, row in df.iterrows():
        doc = nlp.make_doc(row["text"])
        cats = {l: 0 for l in labels}
        cats[row["label"]] = 1
        yield Example.from_dict(doc, {"cats": cats})

all_examples = list(get_examples())
print(f"Training on {len(all_examples)} examples across {len(labels)} categories...")

# Initialize textcat so it can infer output dimensions
nlp.initialize(lambda: all_examples)
optimizer = nlp.resume_training()

# Decaying dropout over 20 epochs (loss converges fast with word vectors)
EPOCHS = 20
dropout_start = 0.4
dropout_end = 0.1
dropout_step = (dropout_start - dropout_end) / EPOCHS

with nlp.select_pipes(enable=["textcat_multilabel"]):
    for epoch in range(EPOCHS):
        random.shuffle(all_examples)
        losses = {}
        drop = max(dropout_end, dropout_start - (epoch * dropout_step))

        # Larger batches = faster GPU utilization
        batches = list(minibatch(all_examples, size=compounding(16.0, 128.0, 1.001)))
        for batch in batches:
            nlp.update(batch, sgd=optimizer, drop=drop, losses=losses)

        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"Epoch {epoch + 1:2d} (drop={drop:.3f}) - Loss: {losses.get('textcat_multilabel', 0):.5f}")

# Save model
nlp.to_disk(str(MODEL_OUTPUT))
print(f"\nTraining completed. Model saved to {MODEL_OUTPUT}")