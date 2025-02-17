import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos

# Agregar una imagen o logo en la barra lateral (opcional)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Vector_biblioteca.png", use_column_width=True)

# Cambiar el diseño del menú lateral
st.sidebar.markdown("### 📌 Navegación")
opcion = st.sidebar.selectbox("", ["Inicio", "Gestión de corpus", "Extracción terminológica", "Validación de términos"])

# ------------------------------
# Funcionalidad 0: Pantalla de Inicio
# ------------------------------
if opcion == "Inicio":
    st.title("📌 App para el trabajo terminográfico")
    st.markdown(
        """
        👋 ¡Hola! Esta es una aplicación diseñada para ayudarte en la gestión y minería de textos, especialmente diseñada para asistirte en el trabajo terminográfico.
        
        🔍 **¿Qué puedes hacer aquí?**
        
        - 📂 **Gestión de corpus** → Subir archivos `.txt` (¡siempre es mejor si está codificado en UTF-8!) y estructurar un corpus con metadatos.
        - 🏷️ **Extracción terminológica** → Extraer términos mediante métodos como **TF-IDF, POS Tagging y C-Value**.
        - ✅ **Validación de términos** → Subir un CSV con términos extraídos (¡el mismo que te genera esta app!) y marcar los términos reales.
        
        📌 **Usa el menú lateral para navegar entre las distintas funciones. ¡Espero que te sirva!.**
        """
    )

# ------------------------------
# Funcionalidad 1: Gestión de corpus
# ------------------------------
elif opcion == "Gestión de corpus":
    gestion_corpus()

# ------------------------------
# Funcionalidad 2: Extracción terminológica
# ------------------------------
elif opcion == "Extracción terminológica":
    extraccion_terminologica()

# ------------------------------
# Funcionalidad 3: Validación de términos
# ------------------------------
elif opcion == "Validación de términos":
    validacion_terminos()
