import spacy
import re
from spacy.lang.en.stop_words import STOP_WORDS

# Cargar modelo de spaCy
nlp = spacy.load("en_core_web_sm")

# Cargar stoplist académica desde archivo externo
def load_academic_stoplist(filepath="academic_stoplist.txt"):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return set(line.strip().lower() for line in file if line.strip())
    except FileNotFoundError:
        return set()

academic_stoplist = load_academic_stoplist()


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
    
    # Eliminar términos compuestos de la stoplist antes de tokenizar
    if apply_custom_stoplist:
        for phrase in academic_stoplist:
            text = re.sub(rf"\b{re.escape(phrase)}\b", "", text)
    
    doc = nlp(text)
    processed_tokens = []
    
    for token in doc:
        if remove_stopwords and token.text.lower() in STOP_WORDS and token.text.lower() != "of":
            continue
        
        if lemmatize_text:
            processed_tokens.append(token.lemma_)
        else:
            processed_tokens.append(token.text)
    
    return " ".join(processed_tokens)
