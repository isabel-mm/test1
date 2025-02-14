import streamlit as st
import spacy
import subprocess
import sys
import pandas as pd
from io import StringIO
from term_extraction import extract_terms_tfidf, extract_terms_pos, extract_terms_cvalue
from preprocessing import preprocess_text

# Verificar si el modelo de spaCy está instalado y descargarlo si no lo está
@st.cache_resource
def load_model():
    model_name = "en_core_web_sm"
    try:
        return spacy.load(model_name)
    except OSError:
        st.warning(f"📥 Descargando el modelo de spaCy '{model_name}', espera unos segundos...")
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
        return spacy.load(model_name)

nlp = load_model()

# Interfaz en Streamlit
st.title("📌 Extracción automática de términos")

st.markdown(
    """ 
    🔍 **Esta aplicación permite extraer términos desde múltiples archivos de texto.**
    
    - 📊 **Método estadístico (TF-IDF):** identifica términos con alta relevancia basándose en su frecuencia e importancia.
    - 📖 **Método lingüístico (POS Tagging):** extrae términos clave utilizando categorías gramaticales (sustantivos, adjetivos, y estructuras específicas).
    - 🔬 **Método híbrido (C-Value):** identifica términos multi-palabra relevantes basándose en su frecuencia y estructura dentro del texto.
    
    📂 **Sube uno o más archivos en texto plano (.txt), configura el preprocesamiento y selecciona un método para la extracción. Luego puedes descargar el listado de candidatos a término en formato .csv.**
    """
)

# Cargar archivos
uploaded_files = st.file_uploader("📎 Carga uno o más archivos .txt", type=["txt"], accept_multiple_files=True, key="file_uploader")

if uploaded_files:
    corpus = ""
    for uploaded_file in uploaded_files:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()
        corpus += text + "\n"
    
    st.success("📂 Corpus cargado correctamente.")
    
    # Opciones de preprocesamiento dentro de un expander
    with st.expander("⚙️ Opciones de preprocesamiento del corpus"):
        apply_lowercase = st.checkbox("Convertir todo a minúsculas")
        remove_stopwords = st.checkbox("Eliminar stopwords en inglés (excepto 'of')")
        lemmatize_text = st.checkbox("Aplicar lematización")
        apply_custom_stoplist = st.checkbox("Aplicar stoplist académica")
    
    # Selección de método de extracción
    method = st.selectbox("🛠️ Selecciona el método de extracción", ["Método estadístico (TF-IDF)", "Método lingüístico (POS)", "Método híbrido (C-Value)"])
    
    # Botón para iniciar la extracción
    if st.button("🚀 Comenzar extracción"):
        # Aplicar preprocesamiento
        with st.spinner("🛠 Aplicando preprocesamiento..."):
            corpus = preprocess_text(corpus, apply_lowercase, remove_stopwords, lemmatize_text, apply_custom_stoplist)
        
        st.text_area("📝 Contenido combinado del corpus (preprocesado):", corpus[:1000] + "...", height=200)
        
        # Aplicar método seleccionado con indicador de carga
        with st.spinner("🔍 Extrayendo términos..."):
            if method == "Método estadístico (TF-IDF)":
                terms = extract_terms_tfidf(corpus)
                st.subheader("📊 Términos extraídos con TF-IDF")
                df_terms = pd.DataFrame(terms[:50], columns=["Término", "Puntaje TF-IDF"])
            elif method == "Método lingüístico (POS)":
                terms = extract_terms_pos(corpus)
                st.subheader("📖 Términos extraídos con POS Tagging (ordenados por frecuencia)")
                df_terms = pd.DataFrame(terms[:50], columns=["Términos extraídos", "Frecuencia"])
            else:
                terms = extract_terms_cvalue(corpus)
                st.subheader("🔬 Términos extraídos con C-Value")
                df_terms = pd.DataFrame(terms[:50], columns=["Términos extraídos", "Puntaje C-Value"])
        
        st.dataframe(df_terms)  # Mostrar los 50 primeros términos en la interfaz
        
        # Botón para descargar términos
        csv = pd.DataFrame(terms, columns=["Términos extraídos", "Frecuencia"]).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar todos los términos como CSV",
            data=csv,
            file_name="terminos_extraidos.csv",
            mime="text/csv"
        )
