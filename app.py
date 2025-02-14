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

# Interfaz en Streamlit
st.title("Extracción de Términos con TF-IDF desde un Archivo de Texto")

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"], key="file_uploader")

if uploaded_file is not None:
    # Leer contenido del archivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text = stringio.read()
    
    st.subheader("Texto cargado")
    st.text_area("Contenido del archivo:", text, height=200)
    
    # Extraer términos con TF-IDF
    terms = extract_terms_tfidf(text)
    
    # Mostrar resultados
    if terms:
        st.subheader("Términos extraídos con TF-IDF")
        df_terms = pd.DataFrame(terms, columns=["Término", "Puntaje TF-IDF"])
        st.dataframe(df_terms)
        
        # Botón para descargar términos
        csv = df_terms.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar términos como CSV",
            data=csv,
            file_name="terminos_tfidf.csv",
            mime="text/csv"
        )
    else:
        st.warning("No se encontraron términos en el archivo.")
