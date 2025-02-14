import streamlit as st
import spacy
import pandas as pd
from io import StringIO

# Cargar modelo de spaCy sin instalación en tiempo de ejecución
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

try:
    nlp = load_model()
except OSError:
    st.error("El modelo de spaCy 'en_core_web_sm' no está instalado. Verifica que esté en 'requirements.txt'.")

# Función para extraer términos
def extract_terms(text):
    doc = nlp(text)
    terms = set()
    
    for chunk in doc.noun_chunks:
        terms.add(chunk.text)
    
    for ent in doc.ents:
        terms.add(ent.text)
    
    return sorted(terms)

# Interfaz en Streamlit
st.title("Extracción de Términos desde un Archivo de Texto")

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"])

if uploaded_file is not None:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text = stringio.read()
    
    st.subheader("Texto cargado")
    st.text_area("Contenido del archivo:", text, height=200)
    
    terms = extract_terms(text)
    
    if terms:
        st.subheader("Términos extraídos")
        df_terms = pd.DataFrame(terms, columns=["Términos extraídos"])
        st.dataframe(df_terms)
        
        csv = df_terms.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar términos como CSV",
            data=csv,
            file_name="terminos_extraidos.csv",
            mime="text/csv"
        )
    else:
        st.warning("No se encontraron términos en el archivo.")
