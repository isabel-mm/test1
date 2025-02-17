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

# Menú lateral para seleccionar la funcionalidad
st.sidebar.title("Menú de opciones")
opcion = st.sidebar.radio("Selecciona una funcionalidad", ["Gestión de corpus", "Extracción terminológica", "Validación de términos"])

# ------------------------------
# Funcionalidad 1: Gestión de corpus
# ------------------------------
if opcion == "Gestión de corpus":
    st.title("📂 Gestión de corpus")

    st.markdown(
        """
        🔍 **Esta funcionalidad permite gestionar un corpus de textos**.  
        
        1. 📎 **Sube uno o más archivos de texto (.txt)**.  
        2. 📝 **Añade metadatos a cada texto** (Autor, Año, Tipo de texto).  
        3. 📊 **Descarga el corpus estructurado en CSV**.  
        """
    )

    uploaded_files = st.file_uploader("📎 Sube archivos .txt para tu corpus", type=["txt"], accept_multiple_files=True)

    if uploaded_files:
        corpus_data = []

        for i, uploaded_file in enumerate(uploaded_files):
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            
            with st.expander(f"📄 {uploaded_file.name}"):
                author = st.text_input(f"✍️ Autor de '{uploaded_file.name}'", key=f"author_{i}")
                year = st.number_input(f"📅 Año de publicación de '{uploaded_file.name}'", min_value=1000, max_value=2100, step=1, key=f"year_{i}")
                text_type = st.selectbox(f"📑 Tipo de texto de '{uploaded_file.name}'", ["Artículo científico", "Ensayo", "Reporte", "Otro"], key=f"type_{i}")

            corpus_data.append({"Archivo": uploaded_file.name, "Texto": text, "Autor": author, "Año": year, "Tipo de texto": text_type})

        df_corpus = pd.DataFrame(corpus_data)
        st.subheader("📊 Corpus estructurado")
        st.dataframe(df_corpus[["Archivo", "Autor", "Año", "Tipo de texto"]])

        csv_corpus = df_corpus.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar Corpus en CSV", data=csv_corpus, file_name="corpus.csv", mime="text/csv")

# ------------------------------
# Funcionalidad 2: Extracción terminológica
# ------------------------------
elif opcion == "Extracción terminológica":
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

    uploaded_files = st.file_uploader("📎 Carga archivos .txt", type=["txt"], accept_multiple_files=True, key="file_uploader")

    if uploaded_files:
        corpus = ""
        for uploaded_file in uploaded_files:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            corpus += text + "\n"

        st.success("📂 Corpus cargado correctamente.")

        method = st.selectbox("🛠️ Selecciona el método de extracción", ["Método estadístico (TF-IDF)", "Método lingüístico (POS)", "Método híbrido (C-Value)"])

        if st.button("🚀 Comenzar extracción"):
            with st.spinner("🔍 Extrayendo términos..."):
                if method == "Método estadístico (TF-IDF)":
                    terms = extract_terms_tfidf(corpus)
                elif method == "Método lingüístico (POS)":
                    terms = extract_terms_pos(corpus)
                else:
                    terms = extract_terms_cvalue(corpus)

            df_terms = pd.DataFrame(terms, columns=["Término", "Frecuencia"])
            st.dataframe(df_terms)

            csv = df_terms.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar términos en CSV", data=csv, file_name="terminos.csv", mime="text/csv")

# ------------------------------
# Funcionalidad 3: Validación de términos
# ------------------------------
elif opcion == "Validación de términos":
    st.title("✅ Validación de términos extraídos")
    
    st.markdown(
        """
        🔍 **Instrucciones para la validación de términos**
        
        📎 **Sube un archivo CSV con los términos extraídos**.
        """
    )

    uploaded_file = st.file_uploader("📎 Sube tu archivo CSV aquí", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "Términos extraídos" not in df.columns:
            st.error("⚠️ El archivo debe contener una columna llamada 'Términos extraídos'.")
        else:
            if "Es término" not in df.columns:
                df["Es término"] = False  

            st.subheader("🔍 Revisión de términos")
            df_editable = st.data_editor(df, num_rows="dynamic", key="term_editor")

            df_validated = df_editable[df_editable["Es término"] == True][["Términos extraídos"]]

            csv_data = df_validated.to_csv(index=False).encode("utf-8")
            txt_data = "\n".join(df_validated["Términos extraídos"])
            json_data = df_validated.to_json(orient="records", indent=4)

            st.subheader("📥 Descargar términos validados")
            st.download_button(label="📥 Descargar CSV", data=csv_data, file_name="terminos_validados.csv", mime="text/csv")
            st.download_button(label="📥 Descargar TXT", data=txt_data, file_name="terminos_validados.txt", mime="text/plain")
            st.download_button(label="📥 Descargar JSON", data=json_data, file_name="terminos_validados.json", mime="application/json")
