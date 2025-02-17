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
opcion = st.sidebar.radio("Selecciona una funcionalidad", ["Gestión de Corpus", "Extracción terminológica", "Validación de términos"])

# ------------------------------
# Funcionalidad 1: Gestión de Corpus
# ------------------------------
if opcion == "Gestión de Corpus":
    st.title("📂 Gestión de Corpus")

    st.markdown(
        """
        🔍 **Esta funcionalidad permite gestionar un corpus de textos**.  
        
        1. 📎 **Sube uno o más archivos de texto (.txt)**.  
        2. 📝 **Añade metadatos a cada texto** (Autor, Año, Tipo de texto).  
        3. 📊 **Descarga el corpus estructurado en CSV**.  
        """
    )

    # Cargar archivos
    uploaded_files = st.file_uploader("📎 Sube archivos .txt para tu corpus", type=["txt"], accept_multiple_files=True)

    if uploaded_files:
        corpus_data = []

        for uploaded_file in uploaded_files:
            # Leer contenido del archivo
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            text = stringio.read()
            
            # Solicitar metadatos para cada archivo
            st.subheader(f"📄 {uploaded_file.name}")
            author = st.text_input(f"✍️ Autor de '{uploaded_file.name}'", key=f"author_{uploaded_file.name}")
            year = st.number_input(f"📅 Año de publicación de '{uploaded_file.name}'", min_value=1000, max_value=2100, step=1, key=f"year_{uploaded_file.name}")
            text_type = st.selectbox(f"📑 Tipo de texto de '{uploaded_file.name}'", ["Artículo científico", "Ensayo", "Reporte", "Otro"], key=f"type_{uploaded_file.name}")

            # Guardar datos
            corpus_data.append({"Archivo": uploaded_file.name, "Texto": text, "Autor": author, "Año": year, "Tipo de texto": text_type})

        # Convertir a DataFrame
        df_corpus = pd.DataFrame(corpus_data)

        # Mostrar tabla con el corpus estructurado
        st.subheader("📊 Corpus estructurado")
        st.dataframe(df_corpus)

        # Botón para descargar corpus en CSV
        csv_corpus = df_corpus.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar Corpus en CSV", data=csv_corpus, file_name="corpus.csv", mime="text/csv")


# ------------------------------
# Funcionalidad 2: Extracción terminológica
# ------------------------------
if opcion == "Extracción terminológica":
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

# ------------------------------
# Funcionalidad 3: Validación de términos
# ------------------------------
elif opcion == "Validación de términos":
    st.title("✅ Validación de términos extraídos")
    
    st.markdown(
        """
        🔍 **Instrucciones para la validación de términos**
        
        1. **Sube un archivo CSV** con los términos extraídos.
        2. **El archivo debe contener al menos una columna llamada "Términos extraídos" (si has utilizado el extractor en esta misma app, ya estará así por defecto)**.
        3. **Opcionalmente**, puede contener una columna "Es término" (con valores `True` o `False`).  
        4. Si la columna "Es término" no está presente, se añadirá automáticamente para que puedas marcar los términos manualmente, ¡no te preocupes!  
        5. Puedes modificar las marcas en la tabla y luego descargar el archivo validado.
        
        📌 **Aquí tienes un ejemplo de estructura esperada del archivo CSV 😊**
        
        | Términos extraídos | Es término |
        |--------------------|------------|
        | aprendizaje automático | True |
        | modelo lingüístico | False |
        | procesamiento del lenguaje natural | True |
        
        """
    )

    # Cargar el CSV
    uploaded_file = st.file_uploader("📎 Sube tu archivo CSV aquí", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Verificar si la columna de términos existe
        if "Términos extraídos" not in df.columns:
            st.error("⚠️ Recuerda, el archivo debe contener una columna llamada 'Términos extraídos'.")
        else:
            # Añadir una columna de validación si no existe
            if "Es término" not in df.columns:
                df["Es término"] = False  # Inicialmente, todos los términos están en False

            # Mostrar los términos en una tabla editable
            st.subheader("🔍 Revisión de términos")
            df_editable = st.data_editor(df, num_rows="dynamic", key="term_editor")

            # Cálculo de precisión: % de términos validados y descartados
            total_terms = len(df_editable)
            validated_terms = df_editable["Es término"].sum()
            discarded_terms = total_terms - validated_terms

            validated_percentage = (validated_terms / total_terms) * 100 if total_terms > 0 else 0
            discarded_percentage = (discarded_terms / total_terms) * 100 if total_terms > 0 else 0

            # Mostrar estadísticas de precisión
            st.subheader("📊 Estadísticas de validación")
            st.write(f"✅ **Términos validados:** {validated_terms} ({validated_percentage:.2f}%)")
            st.write(f"❌ **Términos descartados:** {discarded_terms} ({discarded_percentage:.2f}%)")

            # Gráfico de precisión
            st.bar_chart({"Validado (%)": validated_percentage, "Descartado (%)": discarded_percentage})

            # Filtrar solo los términos validados
            df_validated = df_editable[df_editable["Es término"] == True][["Términos extraídos"]]

            # Formatos de descarga
            csv_data = df_validated.to_csv(index=False).encode("utf-8")
            txt_data = "\n".join(df_validated["Términos extraídos"])
            json_data = df_validated.to_json(orient="records", indent=4)

            # Botones de descarga
            st.subheader("📥 Descargar términos validados")
            st.download_button(label="📥 Descargar CSV", data=csv_data, file_name="terminos_validados.csv", mime="text/csv")
            st.download_button(label="📥 Descargar TXT", data=txt_data, file_name="terminos_validados.txt", mime="text/plain")
            st.download_button(label="📥 Descargar JSON", data=json_data, file_name="terminos_validados.json", mime="application/json")


