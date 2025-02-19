import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter

# Cargar modelo de spaCy para procesamiento del lenguaje
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def calcular_estadisticas(texto):
    """Calcula estadísticas básicas del corpus."""
    if not texto or texto.strip() == "":
        return None  # Si el texto está vacío, devolvemos None

    doc = nlp(texto)
    tokens = [token.text for token in doc]
    palabras = [token.text for token in doc if token.is_alpha]
    tipos_palabras = set(palabras)
    densidad_lexica = len(set([token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]])) / len(tokens) if len(tokens) > 0 else 0
    
    return {
        "Total de tokens": len(tokens),
        "Total de palabras": len(palabras),
        "Palabras únicas (Type)": len(tipos_palabras),
        "Type-Token Ratio (TTR)": len(tipos_palabras) / len(tokens) if len(tokens) > 0 else 0,
        "Densidad léxica": densidad_lexica
    }

def generar_nube_palabras(texto):
    """Genera una nube de palabras a partir del texto."""
    if not texto or texto.strip() == "":
        st.warning("⚠️ No hay texto válido para generar una nube de palabras.")
        return
    
    doc = nlp(texto)
    palabras = [token.text.lower() for token in doc if token.is_alpha]
    
    if not palabras:
        st.warning("⚠️ No hay suficientes palabras para generar una nube de palabras.")
        return
    
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
                texto = archivo.getvalue().decode("utf-8").strip()
                if texto:
                    corpus += texto + "\n"
            elif archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
                if not df.empty:
                    corpus += " ".join(df.astype(str).values.flatten()) + "\n"

    if corpus.strip():  # Verificamos que haya contenido en el corpus antes de procesarlo
        if st.button("📈 Analizar Corpus"):
            stats = calcular_estadisticas(corpus)
            if stats is None:
                st.error("❌ El texto está vacío o no es válido para el análisis.")
                return

            st.subheader("📊 Estadísticas del Corpus")
            df_stats = pd.DataFrame(stats.items(), columns=["Métrica", "Valor"])
            st.dataframe(df_stats)

            st.subheader("☁️ Nube de palabras")
            generar_nube_palabras(corpus)
    else:
        st.warning("⚠️ Carga al menos un archivo válido para analizar el corpus.")
