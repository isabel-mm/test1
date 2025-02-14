import spacy
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

def extract_terms_tfidf(text):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    terms_with_scores = list(zip(feature_array, tfidf_scores))
    terms_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [t for t in terms_with_scores if re.search(r"\w", t[0])]

def extract_terms_pos(text):
    doc = nlp(text.lower())  # Normalizar a minúscula
    term_counts = Counter()
    
    for i, token in enumerate(doc):
        if token.pos_ == "NOUN":
            term = [token.lemma_]
            j = i + 1
            while j < len(doc) and doc[j].pos_ == "NOUN" and len(term) < 3:
                term.append(doc[j].lemma_)
                j += 1
            term_counts[" ".join(term)] += 1
        
        elif token.pos_ == "ADJ":
            term = [token.lemma_]
            j = i + 1
            while j < len(doc) and doc[j].pos_ == "ADJ" and len(term) < 3:
                term.append(doc[j].lemma_)
                j += 1
            if j < len(doc) and doc[j].pos_ == "NOUN":
                term.append(doc[j].lemma_)
                term_counts[" ".join(term)] += 1
        
        elif token.pos_ == "NOUN" and i + 2 < len(doc) and doc[i+1].pos_ == "ADP" and doc[i+1].text.lower() == "of" and doc[i+2].pos_ == "NOUN":
            term = [token.lemma_, "of", doc[i+2].lemma_]
            j = i + 3
            while j < len(doc) and doc[j].pos_ == "NOUN" and len(term) < 5:
                term.append(doc[j].lemma_)
                j += 1
            term_counts[" ".join(term)] += 1
    
    return term_counts.most_common()
