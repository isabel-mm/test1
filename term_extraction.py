import spacy
import re
from collections import Counter
from collections import defaultdict
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

def extract_terms_cvalue(text, min_length=2, max_length=5):
    """
    Extrae términos utilizando el algoritmo C-Value.
    
    :param text: Texto preprocesado de entrada.
    :param min_length: Longitud mínima de los términos candidatos.
    :param max_length: Longitud máxima de los términos candidatos.
    :return: Lista de términos ordenados por su puntuación C-Value.
    """
    doc = nlp(text)
    term_candidates = []
    
    # Extraer n-gramas de longitud entre min_length y max_length
    words = [token.text for token in doc if token.is_alpha]
    for length in range(min_length, max_length + 1):
        for i in range(len(words) - length + 1):
            term_candidates.append(" ".join(words[i:i + length]))
    
    # Contar ocurrencias de cada término
    term_frequencies = Counter(term_candidates)
    
    # Calcular C-Value para cada término
    term_cvalue = {}
    nested_terms = defaultdict(list)
    
    for term in term_frequencies:
        term_cvalue[term] = math.log2(len(term.split())) * term_frequencies[term]
        for longer_term in term_frequencies:
            if term in longer_term and term != longer_term:
                nested_terms[term].append(longer_term)
    
    for term, longer_terms in nested_terms.items():
        nested_count = sum(term_frequencies[t] for t in longer_terms)
        term_cvalue[term] -= nested_count / len(longer_terms) if longer_terms else 0
    
    # Ordenar términos por C-Value
    sorted_terms = sorted(term_cvalue.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_terms[:50]  # Devolver los 50 términos más relevantes

