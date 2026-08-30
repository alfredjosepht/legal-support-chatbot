import sys
sys.path.insert(0, ".")
import random
import spacy
import pandas as pd
from spacy.training.example import Example
from spacy.util import minibatch, compounding, decaying
from collections import defaultdict
from nlp.postprocess import postprocess_categories

random.seed(42)

df = pd.read_csv("data/dataset.csv")
labels = df["label"].unique()

# Load pretrained model with 500k word vectors
nlp = spacy.load("en_core_web_md")

# Remove unused pipes to keep training fast and focused on text classification
for pipe in [p for p in nlp.pipe_names if p != "tok2vec"]:
    nlp.remove_pipe(pipe)

textcat = nlp.add_pipe("textcat_multilabel")
for label in labels:
    textcat.add_label(label)

examples = []
for _, row in df.iterrows():
    doc = nlp.make_doc(row["text"])
    cats = {l: 0 for l in labels}
    cats[row["label"]] = 1
    examples.append(Example.from_dict(doc, {"cats": cats}))

textcat.initialize(lambda: examples, nlp=nlp)
optimizer = nlp.resume_training()

def decaying_dropout(start=0.35, end=0.10, rate=0.01):
    d = start
    while True:
        yield max(end, d)
        d -= rate

dropout = decaying_dropout(0.35, 0.10, 0.01)

print("Training with en_core_web_md + minibatching + decaying dropout...")

for epoch in range(25):
    random.shuffle(examples)
    losses = {}
    drop_rate = next(dropout)
    batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        nlp.update(batch, sgd=optimizer, drop=drop_rate, losses=losses)
    print(f"Epoch {epoch + 1:2d} (drop={drop_rate:.3f}) - Loss: {losses}")

# Evaluate
correct_post = 0
correct_raw = 0
matched_cov = 0
cat_tp = defaultdict(int)
cat_pred = defaultdict(int)
cat_true = defaultdict(int)

for _, row in df.iterrows():
    text = row["text"]
    true_l = row["label"]
    doc = nlp(text)
    raw_cats = doc.cats
    final_cats, _ = postprocess_categories(text, raw_cats)
    
    pred_raw = max(raw_cats, key=raw_cats.get) if raw_cats else "unknown"
    pred_post = max(final_cats, key=final_cats.get) if final_cats else pred_raw
    
    cat_true[true_l] += 1
    cat_pred[pred_post] += 1
    
    if pred_raw == true_l:
        correct_raw += 1
    if pred_post == true_l:
        correct_post += 1
        cat_tp[true_l] += 1
    if true_l in final_cats:
        matched_cov += 1
        
f1_list = []
for c in labels:
    tp = cat_tp[c]
    fp = cat_pred[c] - tp
    fn = cat_true[c] - tp
    p = tp / (tp + fp) if (tp + fp) > 0 else 0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0
    f1_list.append(f1)
    
macro_f1 = sum(f1_list) / len(f1_list)
raw_acc = (correct_raw / len(df)) * 100
post_acc = (correct_post / len(df)) * 100
cov_pct = (matched_cov / len(df)) * 100

print(f"\n[RESULTS] Raw Accuracy: {raw_acc:.2f}% | Pipeline Accuracy: {post_acc:.2f}% | Macro F1: {macro_f1*100:.2f}% | Coverage: {cov_pct:.2f}%")
