import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Cargar modelo de spaCy
nlp = spacy.load("en_core_web_sm")

# Stoplist académica (debes añadir los términos específicos que deseas eliminar)
academic_stoplist = {
    "example", "study", "research", "analysis", "data", "method", "approach",
    "academic journal", "area of research", "area of study", "body of text", "cite as",
    "cite by", "cite in", "conference proceeding", "critical approach", "critical look",
    "current study", "different way", "eg", "et al", "et alii", "etc", "etcetera",
    "field of research", "field of study", "for example", "for instance", "good practice",
    "in addition", "in case", "in order to", "in other word", "in relation",
    "literature review", "main body", "many study", "methodological framework",
    "multiple researcher", "multiple way", "on the one hand", "on the other hand",
    "op cit", "other researcher", "other study", "point of view", "present paper",
    "purpose of study", "recent paper", "research article", "research paper",
    "research question", "same way", "scientific journal", "theoretical framework",
    "this paper", "university press", "variety of way", "work to date",
    "special issue", "in particular", "related work", "previous work"
}
stop_words_set = set(STOP_WORDS)  # Convertir en conjunto para búsqueda más rápida


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
    if not text.strip():  # Verificar que el texto no esté vacío
        return ""
    
    if apply_lowercase:
        text = text.lower()
    
    doc = nlp(text)
    processed_tokens = []
    
    for token in doc:
        if remove_stopwords and token.text.lower() in stop_words_set and token.text.lower() != "of":
            continue
        
        if apply_custom_stoplist and token.text.lower() in academic_stoplist:
            continue
        
        if lemmatize_text:
            processed_tokens.append(token.lemma_)
        else:
            processed_tokens.append(token.text)
    
    return " ".join(processed_tokens).strip()  # Remover espacios extra
