import streamlit as st
import spacy
import subprocess
import sys
import pandas as pd
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer

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
    
    return terms_with_scores[:20]  # Extrae los 20 términos más relevantes

# Función para extraer términos clave con POS tagging y lematización
def extract_terms_pos(text):
    doc = nlp(text.lower())  # Normalizar a minúscula
    terms = set()
    
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop:
            terms.add(token.lemma_)
    
    return sorted(terms)[:20]  # Extrae los 20 términos más frecuentes

# Interfaz en Streamlit
st.title("Extracción de Términos desde un Archivo de Texto")

# Selección de método de extracción
method = st.selectbox("Selecciona el método de extracción", ["TF-IDF", "POS Tagging"])

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"], key="file_uploader")

if uploaded_file is not None and method:
    # Leer contenido del archivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text = stringio.read()
    
    st.subheader("Texto cargado")
    st.text_area("Contenido del archivo:", text, height=200)
    
    # Aplicar método seleccionado
    if method == "TF-IDF":
        terms = extract_terms_tfidf(text)
        st.subheader("Términos extraídos con TF-IDF")
        df_terms = pd.DataFrame(terms, columns=["Término", "Puntaje TF-IDF"])
    else:
        terms = extract_terms_pos(text)
        st.subheader("Términos extraídos con POS Tagging")
        df_terms = pd.DataFrame(terms, columns=["Términos extraídos"])
    
    st.dataframe(df_terms)
    
    # Botón para descargar términos
    csv = df_terms.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Descargar términos como CSV",
        data=csv,
        file_name="terminos_extraidos.csv",
        mime="text/csv"
    )
