import streamlit as st
import spacy
import subprocess
import sys
import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from collections import Counter

# Verificar si el modelo de spaCy está instalado y descargarlo si no lo está
@st.cache_resource
def load_model():
    model_name = "en_core_web_sm"
    try:
        return spacy.load(model_name)
    except OSError:
        st.warning(f"Descargando el modelo de spaCy '{model_name}', espera unos segundos...")
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
        return spacy.load(model_name)

nlp = load_model()

# Función para extraer términos clave con TF-IDF
def extract_terms_tfidf(text):
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_array = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    terms_with_scores = list(zip(feature_array, tfidf_scores))
    terms_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    return [t for t in terms_with_scores[:50] if re.search(r"\w", t[0])]  # Filtrar términos vacíos o caracteres especiales

# Función para extraer términos clave con POS tagging y lematización
def extract_terms_pos(text):
    doc = nlp(text.lower())  # Normalizar a minúscula
    term_counts = Counter()
    
    for i, token in enumerate(doc):
        # NOUN (hasta 3 seguidos)
        if token.pos_ == "NOUN":
            term = [token.lemma_]
            j = i + 1
            while j < len(doc) and doc[j].pos_ == "NOUN" and len(term) < 3:
                term.append(doc[j].lemma_)
                j += 1
            term_counts[" ".join(term)] += 1
        
        # ADJ (hasta 3) + NOUN
        elif token.pos_ == "ADJ":
            term = [token.lemma_]
            j = i + 1
            while j < len(doc) and doc[j].pos_ == "ADJ" and len(term) < 3:
                term.append(doc[j].lemma_)
                j += 1
            if j < len(doc) and doc[j].pos_ == "NOUN":
                term.append(doc[j].lemma_)
                term_counts[" ".join(term)] += 1
        
        # NOUN + PREP ('of') + NOUN (hasta 3)
        elif token.pos_ == "NOUN" and i + 2 < len(doc) and doc[i+1].pos_ == "ADP" and doc[i+1].text.lower() == "of" and doc[i+2].pos_ == "NOUN":
            term = [token.lemma_, "of", doc[i+2].lemma_]
            j = i + 3
            while j < len(doc) and doc[j].pos_ == "NOUN" and len(term) < 5:
                term.append(doc[j].lemma_)
                j += 1
            term_counts[" ".join(term)] += 1
    
    # Ordenar términos por frecuencia y devolver los más frecuentes
    return term_counts.most_common(50)

# Interfaz en Streamlit
st.title("Extracción de Términos desde un Archivo de Texto")

# Selección de método de extracción
method = st.selectbox("Selecciona el método de extracción", ["Método estadístico (TF-IDF)", "Método lingüístico (POS)"])

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"], key="file_uploader")

if uploaded_file is not None and method:
    # Leer contenido del archivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text = stringio.read()
    
    st.subheader("Texto cargado")
    st.text_area("Contenido del archivo:", text, height=200)
    
    # Aplicar método seleccionado
    if method == "Método estadístico (TF-IDF)":
        terms = extract_terms_tfidf(text)
        st.subheader("Términos extraídos con TF-IDF")
        df_terms = pd.DataFrame(terms, columns=["Término", "Puntaje TF-IDF"])
    else:
        terms = extract_terms_pos(text)
        st.subheader("Términos extraídos con POS Tagging (ordenados por frecuencia)")
        df_terms = pd.DataFrame(terms, columns=["Términos extraídos", "Frecuencia"])
    
    st.dataframe(df_terms.head(50))  # Mostrar solo los 50 primeros términos en la interfaz
    
    # Botón para descargar términos
    csv = df_terms.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar términos como CSV",
        data=csv,
        file_name="terminos_extraidos.csv",
        mime="text/csv"
    )
