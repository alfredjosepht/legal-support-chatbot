import spacy
print("spacy ok")
nlp = spacy.load("en_core_web_md", exclude=["tagger","parser","ner","senter","attribute_ruler","lemmatizer"])
print("loaded ok")
print("vocab size:", len(nlp.vocab))
print("has vectors:", nlp.vocab.vectors.shape)
