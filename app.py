import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from visualizador_corpus import visualizador_corpus  # Ahora es la funcionalidad 2
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos
from acerca_de import acerca_de

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# 📌 Menú lateral con un selector de navegación
st.sidebar.markdown("### Navegador")

opcion = st.sidebar.radio(
    "Selecciona una funcionalidad:",
    ["Inicio", "Gestión de corpus", "Visualizador de corpus", "Extracción terminológica", "Validación de términos", "Acerca de"],
    index=["Inicio", "Gestión de corpus", "Visualizador de corpus", "Extracción terminológica", "Validación de términos", "Acerca de"].index(st.session_state.pagina)
)

# Actualizar la página seleccionada
st.session_state.pagina = opcion

# ------------------------------
# Funcionalidad 0: Pantalla de Inicio
# ------------------------------
if st.session_state.pagina == "Inicio":
    st.title("TermoLing, una estación de trabajo terminográfico")
    st.markdown(
        """
        Esta es una aplicación creada para la gestión y minería de textos, especialmente diseñada para el trabajo terminográfico.
        
        **¿Qué puedes hacer aquí?**
        
        - **Gestión de corpus** → Subir archivos `.txt` (codificados en UTF-8) y estructurar un corpus con metadatos.
        - **Visualización de corpus** → Analizar corpus con estadísticas y nubes de palabras.
        - **Extracción terminológica** → Extraer términos mediante métodos como **TF-IDF, POS Tagging y C-Value**.
        - **Validación de términos** → Subir un archivo `.csv` con términos extraídos y validar los candidatos a término.
        
        Usa el menú lateral para navegar entre las distintas funciones.
        """
    )

# ------------------------------
# Funcionalidad 1: Gestión de corpus
# ------------------------------
elif st.session_state.pagina == "Gestión de corpus":
    gestion_corpus()

# ------------------------------
# Funcionalidad 2: Visualizador de corpus
# ------------------------------
elif st.session_state.pagina == "Visualizador de corpus":
    visualizador_corpus()

# ------------------------------
# Funcionalidad 3: Extracción terminológica
# ------------------------------
elif st.session_state.pagina == "Extracción terminológica":
    extraccion_terminologica()

# ------------------------------
# Funcionalidad 4: Validación de términos
# ------------------------------
elif st.session_state.pagina == "Validación de términos":
    validacion_terminos()

# ------------------------------
# Funcionalidad 5: Acerca de
# ------------------------------
elif st.session_state.pagina == "Acerca de":
    acerca_de()
