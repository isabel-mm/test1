import streamlit as st
import spacy
import subprocess
import sys
import pandas as pd
from io import StringIO

# Verificar si el modelo está instalado y descargarlo si no lo está
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

uploaded_file = st.file_uploader("Carga un archivo .txt", type=["txt"], key="file_uploader")

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
