import streamlit as st
import pandas as pd
from term_extraction import extract_terms_tfidf, extract_terms_pos, extract_terms_cvalue
from preprocessing import preprocess_text
from io import StringIO

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
