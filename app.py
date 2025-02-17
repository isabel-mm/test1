import streamlit as st
import spacy
import subprocess
import sys
import pandas as pd
import matplotlib.pyplot as plt
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
opcion = st.sidebar.radio("Selecciona una funcionalidad", ["Extracción terminológica", "Validación de términos"])

# ------------------------------
# Funcionalidad 1: Extracción terminológica
# ------------------------------
if opcion == "Extracción terminológica":
    st.title("📌 Extracción automática de términos")

    st.markdown(
        """ 
        🔍 **Esta aplicación permite extraer términos desde múltiples archivos de texto.**
        
        📂 **Sube archivos .txt, selecciona el método de extracción y descarga los términos extraídos.**
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

        # Opciones de preprocesamiento
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

            # Aplicar método seleccionado
            with st.spinner("🔍 Extrayendo términos..."):
                if method == "Método estadístico (TF-IDF)":
                    terms = extract_terms_tfidf(corpus)
                    st.subheader("📊 Términos extraídos con TF-IDF")
                    df_terms = pd.DataFrame(terms[:50], columns=["Término", "Puntaje TF-IDF"])
                elif method == "Método lingüístico (POS)":
                    terms = extract_terms_pos(corpus)
                    st.subheader("📖 Términos extraídos con POS Tagging")
                    df_terms = pd.DataFrame(terms[:50], columns=["Términos extraídos", "Frecuencia"])
                else:
                    terms = extract_terms_cvalue(corpus)
                    st.subheader("🔬 Términos extraídos con C-Value")
                    df_terms = pd.DataFrame(terms[:50], columns=["Términos extraídos", "Puntaje C-Value"])

            st.dataframe(df_terms)

            # Descargar términos en CSV
            csv = pd.DataFrame(terms, columns=["Términos extraídos", "Frecuencia"]).to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Descargar términos (CSV)", data=csv, file_name="terminos_extraidos.csv", mime="text/csv")

# ------------------------------
# Funcionalidad 2: Validación de términos
# ------------------------------
elif opcion == "Validación de términos":
    st.title("✅ Validación de términos extraídos")

    st.markdown(
        """
        🔍 **Instrucciones para la validación de términos**
        
        📎 **Sube un archivo CSV con los términos extraídos**.
        """
    )

    uploaded_file = st.file_uploader("📎 Carga el archivo CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Verificar si la columna de términos existe
        if "Términos extraídos" not in df.columns:
            st.error("⚠️ El archivo debe contener una columna llamada 'Términos extraídos'.")
        else:
            # Añadir una columna de validación si no existe
            if "Es término" not in df.columns:
                df["Es término"] = False

            # Filtros avanzados
            st.subheader("🎯 Filtros de visualización")
            search_term = st.text_input("🔎 Buscar un término específico:")
            show_unvalidated = st.checkbox("Mostrar solo términos no validados")

            if search_term:
                df = df[df["Términos extraídos"].str.contains(search_term, case=False, na=False)]

            if show_unvalidated:
                df = df[df["Es término"] == False]

            # Tabla interactiva
            st.subheader("🔍 Revisión de términos")
            df_editable = st.data_editor(df, num_rows="dynamic", key="term_editor")

            # Estadísticas básicas
            st.subheader("📊 Estadísticas de términos validados")
            df_validated = df_editable[df_editable["Es término"] == True]
            st.write(f"📌 **Número total de términos validados:** {len(df_validated)}")

            # Gráfico de barras de términos más frecuentes
            fig, ax = plt.subplots()
            df_validated["Términos extraídos"].value_counts().head(10).plot(kind="bar", ax=ax)
            ax.set_title("🔝 Términos más frecuentes")
            ax.set_xlabel("Término")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)

            # Opciones de descarga
            st.subheader("📥 Descargar términos validados")

            # CSV
            csv_validated = df_validated.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", data=csv_validated, file_name="terminos_validados.csv", mime="text/csv")

            # JSON
            json_data = df_validated.to_json(orient="records", indent=4)
            st.download_button("📥 Descargar JSON", data=json_data, file_name="terminos_validados.json", mime="application/json")

            # TXT
            txt_data = "\n".join(df_validated["Términos extraídos"])
            st.download_button("📥 Descargar TXT", data=txt_data, file_name="terminos_validados.txt", mime="text/plain")
