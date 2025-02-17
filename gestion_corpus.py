import streamlit as st
import pandas as pd
from io import StringIO

def gestion_corpus():
    st.title("📂 Gestión de corpus")
    
    st.markdown(
        """
        🔍 **Esta funcionalidad permite gestionar un corpus de textos.**  
        
        1. 📎 **Sube tus archivos de texto (.txt), preferiblemente en codificación UTF-8.**  
        2. 📝 **Añade metadatos a cada texto** (autor, año y tipo de texto).  
        3. 📊 **Descarga el corpus estructurado en CSV.**  
        """
    )

    uploaded_files = st.file_uploader("📎 Sube archivos .txt", type=["txt"], accept_multiple_files=True)

    if uploaded_files:
        corpus_data = []
        for i, uploaded_file in enumerate(uploaded_files):
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            
            with st.expander(f"📄 {uploaded_file.name}"):
                author = st.text_input(f"✍️ Autor de '{uploaded_file.name}'", key=f"author_{i}")
                year = st.number_input(f"📅 Año de publicación", min_value=1000, max_value=2100, step=1, key=f"year_{i}")
                text_type = st.selectbox(f"📑 Tipo de texto", ["Artículo de revista", "Capítulo de libro", "Libro", "Reseña", "Otro"], key=f"type_{i}")

            corpus_data.append({"Archivo": uploaded_file.name, "Texto": text, "Autor": author, "Año": year, "Tipo de texto": text_type})

        df_corpus = pd.DataFrame(corpus_data)
        st.subheader("📊 Corpus estructurado")
        st.dataframe(df_corpus[["Archivo", "Autor", "Año", "Tipo de texto"]])

        csv_corpus = df_corpus.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar Corpus en CSV", data=csv_corpus, file_name="corpus.csv", mime="text/csv")
