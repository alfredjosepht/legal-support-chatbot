import spacy
from nlp.postprocess_v2 import postprocess_categories
import traceback
with open("test_out.txt", "w") as f:
    try:
        f.write("Loading spacy\n")
        nlp = spacy.load('models/legal_textcat')
        text = 'my senior raped me'
        f.write("Running nlp\n")
        doc = nlp(text)
        f.write("RAW CATS: " + str(doc.cats) + "\n")
        final, ctx = postprocess_categories(text, doc.cats)
        f.write("FINAL CATS: " + str(final) + "\n")
    except Exception as e:
        f.write("ERROR: " + str(e) + "\n")
        f.write(traceback.format_exc())
