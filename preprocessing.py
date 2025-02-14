import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Cargar modelo de spaCy
nlp = spacy.load("en_core_web_sm")

# Stoplist académica (debes añadir los términos específicos que deseas eliminar)
academic_stoplist = set(["example", "study", "research", "analysis", "data", "method", "approach"])


def preprocess_text(text, apply_lowercase=True, remove_stopwords=True, lemmatize_text=True, apply_custom_stoplist=True):
    """
    Preprocesa un texto según las opciones seleccionadas.
    
    :param text: Texto de entrada.
    :param apply_lowercase: Convierte el texto a minúsculas.
    :param remove_stopwords: Elimina stopwords en inglés (excepto 'of').
    :param lemmatize_text: Aplica lematización.
    :param apply_custom_stoplist: Aplica una stoplist académica personalizada.
    :return: Texto preprocesado.
    """
    if apply_lowercase:
        text = text.lower()
    
    doc = nlp(text)
    processed_tokens = []
    
    for token in doc:
        if remove_stopwords and token.text.lower() in STOP_WORDS and token.text.lower() != "of":
            continue
        
        if apply_custom_stoplist and token.text.lower() in academic_stoplist:
            continue
        
        if lemmatize_text:
            processed_tokens.append(token.lemma_)
        else:
            processed_tokens.append(token.text)
    
    return " ".join(processed_tokens)
