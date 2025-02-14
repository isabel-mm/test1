import streamlit as st
import spacy
import pandas as pd
from io import StringIO

# Cargar modelo spaCy (sin intentos de instalación en tiempo de ejecución)
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

try:
    nlp = load_model()
except OSError:
    st.error("El modelo de spaCy 'en_core_web_sm' no está instalado. Asegúrate de incluirlo en 'requirements.txt'.")

# Función para extraer términos
def extract_terms(text):
    doc = nlp(text)
    terms = set()
    
    # Extraer noun chunks y entidades nombradas
    for chunk in doc.noun_chunks:
        terms.add(chunk.text)
    
    for ent in doc.ents:
        terms.add(ent.text)
    
    return sorted(terms)

# Interfaz en Streamlit
st.title("Extracción de Términos desde un Archivo de Texto")

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"])

if uploaded_file is not None:
    # Leer contenido del archivo
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    text = stringio.read()
    
    st.subheader("Texto cargado")
    st.text_area("Contenido del archivo:", text, height=200)
    
    # Extraer términos
    terms = extract_terms(text)
    
    # Mostrar resultados
    if terms:
        st.subheader("Términos extraídos")
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
    else:
        st.warning("No se encontraron términos en el archivo.")
