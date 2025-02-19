import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter
from io import BytesIO  # Para manejar la descarga de imágenes

# Cargar modelo de spaCy con instalación automática si falta
@st.cache_resource
def load_spacy_model():
    model_name = "en_core_web_sm"
    try:
        return spacy.load(model_name, disable=["parser", "ner"])  # Deshabilitamos parser y NER
    except OSError:
        st.warning(f"📥 Descargando el modelo de spaCy '{model_name}', espera unos segundos...")
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name], check=True)
        return spacy.load(model_name, disable=["parser", "ner"])

nlp = load_spacy_model()
nlp.max_length = 5_000_000  # 🔹 Soporta hasta 5 millones de caracteres
stop_words = nlp.Defaults.stop_words  # 🔹 Lista de stopwords en inglés

def calcular_estadisticas(texto):
    """Calcula estadísticas básicas del corpus."""
    if not isinstance(texto, str) or not texto.strip():
        return None  

    if len(texto) > nlp.max_length:
        st.error(f"❌ El texto es demasiado largo ({len(texto)} caracteres). Reduce el tamaño o usa un corpus más pequeño.")
        return None

    try:
        doc = nlp(texto[:nlp.max_length])  # 🔹 Cortamos el texto si es demasiado largo
    except Exception as e:
        st.error(f"⚠️ Error procesando el texto con spaCy: {e}")
        return None

    tokens = [token.text for token in doc]
    palabras = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words]
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
    """Genera y devuelve una imagen de nube de palabras basada en el corpus."""
    if not isinstance(texto, str) or not texto.strip():
        st.warning("⚠️ No hay texto válido para generar una nube de palabras.")
        return None

    try:
        doc = nlp(texto[:nlp.max_length])  
    except Exception as e:
        st.error(f"⚠️ Error procesando el texto con spaCy: {e}")
        return None

    palabras = [token.text.lower() for token in doc if token.is_alpha and token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"] and token.text.lower() not in stop_words]
    
    if not palabras:
        st.warning("⚠️ No hay suficientes palabras de contenido para generar una nube de palabras.")
        return None

    frecuencia = Counter(palabras)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frecuencia)

    # Guardamos la imagen en memoria para permitir la descarga
    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(buffer, format="png")  # Guardamos la imagen en formato PNG
    buffer.seek(0)
    
    return buffer

def visualizador_corpus():
    st.title("📊 Visualizador de Corpus")
    
    st.markdown(
        """
        🔍 **Este módulo permite analizar corpus lingüísticos:**
        - **Genera una nube de palabras** basada en el texto (sin palabras funcionales).
        - **Muestra estadísticas básicas del corpus** como número total de palabras, diversidad léxica y TTR.
        - **Admite múltiples archivos en formato .txt o .csv**.
        """
    )

    archivos = st.file_uploader("📂 Carga archivos de texto o CSV", type=["txt", "csv"], accept_multiple_files=True)

    corpus = ""
    if archivos:
        for archivo in archivos:
            if archivo.name.endswith(".txt"):
                texto = archivo.getvalue().decode("utf-8", errors="ignore").strip()
                if texto:
                    corpus += texto + "\n"
            elif archivo.name.endswith(".csv"):
                df = pd.read_csv(archivo)
                if not df.empty:
                    corpus += " ".join(df.astype(str).values.flatten()) + "\n"

    corpus = corpus.strip()  

    if corpus:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📊 Generar estadísticas"):
                stats = calcular_estadisticas(corpus)
                if stats:
                    df_stats = pd.DataFrame(stats.items(), columns=["Métrica", "Valor"])
                    st.dataframe(df_stats)

                    # 🔹 Botón para descargar estadísticas en CSV
                    csv_stats = df_stats.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Descargar estadísticas en CSV", data=csv_stats, file_name="estadisticas_corpus.csv", mime="text/csv")

        with col2:
            if st.button("☁️ Generar nube de palabras"):
                buffer = generar_nube_palabras(corpus)
                if buffer:
                    st.image(buffer, caption="Nube de palabras", use_column_width=True)

                    # 🔹 Botón para descargar la nube de palabras
                    st.download_button("📥 Descargar nube de palabras", data=buffer, file_name="nube_palabras.png", mime="image/png")
    else:
        st.warning("⚠️ Carga al menos un archivo válido para analizar el corpus.")
