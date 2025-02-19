import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter

# Cargar modelo de spaCy para procesamiento del lenguaje
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_news_sm")

nlp = load_spacy_model()


def calcular_estadisticas(texto):
    """Calcula estadísticas básicas del corpus."""
    doc = nlp(texto)
    tokens = [token.text for token in doc]
    palabras = [token.text for token in doc if token.is_alpha]
    tipos_palabras = set(palabras)
    densidad_lexica = len(set([token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]])) / len(tokens)
    
    return {
        "Total de tokens": len(tokens),
        "Total de palabras": len(palabras),
        "Palabras únicas (Type)": len(tipos_palabras),
        "Type-Token Ratio (TTR)": len(tipos_palabras) / len(tokens),
        "Densidad léxica": densidad_lexica
    }


def generar_nube_palabras(texto):
    """Genera una nube de palabras a partir del texto."""
    doc = nlp(texto)
    palabras = [token.text.lower() for token in doc if token.is_alpha]
    frecuencia = Counter(palabras)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frecuencia)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)


def visualizador_corpus():
    st.title("📊 Visualizador de Corpus")
    
    st.markdown(
        """
        🔍 **Este módulo permite analizar corpus lingüísticos:**
        - **Genera una nube de palabras** a partir del texto.
        - **Muestra estadísticas básicas del corpus** como número total de palabras, diversidad léxica y TTR.
        - **Admite múltiples archivos en formato .txt o .csv**.
        """
    )
    
    archivos = st.file_uploader("📂 Carga archivos de texto o CSV", type=["txt", "csv"], accept_multiple_files=True)
    
    corpus = ""
    if archivos:
        for archivo in archivos:
            if archivo.name.endswith(".txt"):
                corpus += archivo.getvalue().decode("utf-8") + "\n"
            elif archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
                corpus += " ".join(df.astype(str).values.flatten()) + "\n"
    
    if corpus:
        if st.button("📈 Analizar Corpus"):
            # Calcular estadísticas
            stats = calcular_estadisticas(corpus)
            st.subheader("📊 Estadísticas del Corpus")
            df_stats = pd.DataFrame(stats.items(), columns=["Métrica", "Valor"])
            st.dataframe(df_stats)
            
            # Generar nube de palabras
            st.subheader("☁️ Nube de palabras")
            generar_nube_palabras(corpus)
    else:
        st.warning("⚠️ Carga al menos un archivo para analizar el corpus.")
