import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# Agregar una imagen o logo en la barra lateral (opcional)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/Vector_biblioteca.png", use_container_width=True)

# Cambiar el diseño del menú lateral con botones
st.sidebar.markdown("### 📌 Navegación")

if st.sidebar.button("🏠 Inicio"):
    st.session_state.pagina = "Inicio"
if st.sidebar.button("📂 Gestión de corpus"):
    st.session_state.pagina = "Gestión de corpus"
if st.sidebar.button("📊 Extracción terminológica"):
    st.session_state.pagina = "Extracción terminológica"
if st.sidebar.button("✅ Validación de términos"):
    st.session_state.pagina = "Validación de términos"

# ------------------------------
# Funcionalidad 0: Pantalla de Inicio
# ------------------------------
if st.session_state.pagina == "Inicio":
    st.title("📌 App para el trabajo terminográfico")
    st.markdown(
        """
        👋 ¡Hola! Esta es una aplicación diseñada para ayudarte en la gestión y minería de textos, especialmente diseñada para asistirte en el trabajo terminográfico.
        
        🔍 **¿Qué puedes hacer aquí?**
        
        - 📂 **Gestión de corpus** → Subir archivos `.txt` (¡siempre es mejor si está codificado en UTF-8!) y estructurar un corpus con metadatos.
        - 🏷️ **Extracción terminológica** → Extraer términos mediante métodos como **TF-IDF, POS Tagging y C-Value**.
        - ✅ **Validación de términos** → Subir un CSV con términos extraídos (¡el mismo que te genera esta app!) y marcar los términos reales.
        
        📌 **Usa el menú lateral para navegar entre las distintas funciones. ¡Espero que te sirva!**
        """
    )

# ------------------------------
# Funcionalidad 1: Gestión de corpus
# ------------------------------
elif st.session_state.pagina == "Gestión de corpus":
    gestion_corpus()

# ------------------------------
# Funcionalidad 2: Extracción terminológica
# ------------------------------
elif st.session_state.pagina == "Extracción terminológica":
    extraccion_terminologica()

# ------------------------------
# Funcionalidad 3: Validación de términos
# ------------------------------
elif st.session_state.pagina == "Validación de términos":
    validacion_terminos()
