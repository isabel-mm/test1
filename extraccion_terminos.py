import streamlit as st
import pandas as pd
import spacy
import re
from term_extraction import extract_terms_tfidf, extract_terms_pos, extract_terms_cvalue
from io import StringIO

# Cargar modelo de spaCy con caché para evitar recargas innecesarias
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

# 📌 Función de preprocesamiento
def preprocess_text(text, apply_lowercase, remove_stopwords, lemmatize_text, stoplist):
    """Preprocesa el texto según las opciones seleccionadas por el usuario."""
    doc = nlp(text)
    
    processed_tokens = []
    for token in doc:
        if remove_stopwords and token.is_stop:
            continue
        if lemmatize_text:
            token_text = token.lemma_
        else:
            token_text = token.text.lower() if apply_lowercase else token.text
        
        if stoplist and token_text in stoplist:
            continue
        
        processed_tokens.append(token_text)
    
    return " ".join(processed_tokens)


# 📌 Función principal para la extracción terminológica en Streamlit
def extraccion_terminologica():
    st.title("📌 Extracción automática de términos")

    st.markdown(
        """ 
        🔍 **Esta aplicación permite extraer términos desde múltiples archivos de texto.**
        
        - 📊 **Método estadístico (TF-IDF)**: identifica términos con alta relevancia basándose en su frecuencia e importancia.
        - 📖 **Método lingüístico (POS Tagging)**: extrae términos clave utilizando categorías gramaticales.
        - 🔬 **Método híbrido (C-Value)**: identifica términos multi-palabra basándose en su estructura y frecuencia.
        
        📂 **Sube archivos .txt, selecciona el método de extracción y descarga los términos en formato CSV.**
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

        # 📌 Opciones de preprocesamiento
        with st.expander("⚙️ Opciones de preprocesamiento del corpus"):
            apply_lowercase = st.checkbox("Convertir todo a minúsculas")
            remove_stopwords = st.checkbox("Eliminar stopwords en inglés")
            lemmatize_text = st.checkbox("Aplicar lematización")
            apply_custom_stoplist = st.checkbox("Aplicar stoplist personalizada")

            stoplist = set()
            if apply_custom_stoplist:
                stoplist_input = st.text_area("Introduce palabras a excluir (separadas por comas)", "")
                stoplist = set(stoplist_input.split(","))

        # Aplicar preprocesamiento
        with st.spinner("🛠 Aplicando preprocesamiento..."):
            corpus = preprocess_text(corpus, apply_lowercase, remove_stopwords, lemmatize_text, stoplist)

        # Selección de método de extracción
        method = st.selectbox("🛠️ Selecciona el método de extracción", ["Método estadístico (TF-IDF)", "Método lingüístico (POS)", "Método híbrido (C-Value)"])

        # Botón para iniciar la extracción
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

            # Descargar resultados en CSV
            csv = df_terms.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar términos en CSV", data=csv, file_name="terminos.csv", mime="text/csv")
