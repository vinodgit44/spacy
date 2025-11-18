import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

def analyze(text: str):
    doc = nlp(text)

    return {
        "tokens": [t.text for t in doc],
        "pos_tags": [(t.text, t.pos_) for t in doc],
        "ner": [(ent.text, ent.label_) for ent in doc.ents],
        "dependencies": [(t.text, t.dep_, t.head.text) for t in doc],
        "lemmas": [(t.text, t.lemma_) for t in doc],
        "without_stopwords": [t.text for t in doc if not t.is_stop and t.is_alpha],
    }
