import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from collections import Counter
from io import BytesIO

# Cargar modelo de spaCy para procesamiento del lenguaje
@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

nlp = load_spacy_model()
stop_words = set(nlp.Defaults.stop_words)  # Lista de stopwords en inglés

def dividir_texto(texto, tamano_maximo=1_000_000):
    """Divide el texto en fragmentos más pequeños para evitar el límite de spaCy."""
    fragmentos = [texto[i : i + tamano_maximo] for i in range(0, len(texto), tamano_maximo)]
    st.write(f"🔍 Se dividió el texto en {len(fragmentos)} fragmentos.")  # Depuración
    return fragmentos

def calcular_estadisticas(texto):
    """Calcula estadísticas básicas del corpus en fragmentos."""
    if not isinstance(texto, str) or not texto.strip():
        st.error("❌ El texto está vacío o no es válido.")
        return None  

    fragmentos = dividir_texto(texto)
    total_tokens, total_palabras, total_tipos = 0, 0, set()
    total_palabras_contenido = set()

    for fragmento in fragmentos:
        doc = nlp(fragmento)
        tokens = [token.text for token in doc]
        palabras = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words]
        total_tokens += len(tokens)
        total_palabras += len(palabras)
        total_tipos.update(palabras)
        total_palabras_contenido.update([token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]])

    st.write("✅ Estadísticas calculadas con éxito.")  # Depuración

    return {
        "Total de tokens": total_tokens,
        "Total de palabras": total_palabras,
        "Palabras únicas (Type)": len(total_tipos),
        "Type-Token Ratio (TTR)": len(total_tipos) / total_tokens if total_tokens > 0 else 0,
        "Densidad léxica": len(total_palabras_contenido) / total_tokens if total_tokens > 0 else 0
    }

def generar_nube_palabras(texto):
    """Genera una nube de palabras sin sobrepasar el límite de spaCy."""
    if not isinstance(texto, str) or not texto.strip():
        st.warning("⚠️ No hay texto válido para generar una nube de palabras.")
        return None

    fragmentos = dividir_texto(texto)
    palabras_totales = []

    for fragmento in fragmentos:
        doc = nlp(fragmento)
        palabras = [token.text.lower() for token in doc if token.is_alpha and token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"] and token.text.lower() not in stop_words]
        palabras_totales.extend(palabras)

    if not palabras_totales:
        st.warning("⚠️ No hay suficientes palabras de contenido para generar una nube de palabras.")
        return None

    frecuencia = Counter(palabras_totales)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frecuencia)

    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return buffer

def visualizador_corpus():
    """Interfaz del visualizador de corpus en Streamlit."""
    st.title("📊 Visualizador de Corpus")
    
    st.markdown(
        """
        🔍 **Este módulo permite analizar corpus lingüísticos:**
        - **Genera una nube de palabras** basada en términos de contenido.
        - **Muestra estadísticas básicas del corpus**, como número total de palabras, diversidad léxica y TTR.
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

    if corpus.strip():  
        if st.button("📊 Generar estadísticas"):
            st.write("📢 Procesando estadísticas...")  # Depuración
            stats = calcular_estadisticas(corpus)
            if stats is None:
                st.error("❌ El texto está vacío o no es válido para el análisis.")
                return

            st.subheader("📊 Estadísticas del Corpus")
            df_stats = pd.DataFrame(stats.items(), columns=["Métrica", "Valor"])
            st.dataframe(df_stats)

            # Permitir descarga de estadísticas
            csv_stats = df_stats.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Descargar estadísticas en CSV",
                data=csv_stats,
                file_name="estadisticas_corpus.csv",
                mime="text/csv"
            )

        if st.button("☁️ Generar nube de palabras"):
            st.write("📢 Generando nube de palabras...")  # Depuración
            nube_buffer = generar_nube_palabras(corpus)
            if nube_buffer:
                st.subheader("☁️ Nube de palabras")
                st.image(nube_buffer, use_column_width=True)

                # Botón para descargar la imagen de la nube de palabras
                st.download_button(
                    label="📥 Descargar nube de palabras",
                    data=nube_buffer,
                    file_name="nube_palabras.png",
                    mime="image/png"
                )
    else:
        st.warning("⚠️ Carga al menos un archivo válido para analizar el corpus.")
