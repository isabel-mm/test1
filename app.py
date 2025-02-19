import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from visualizador_corpus import visualizador_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos
from acerca_de import acerca_de 

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# 🔹 CSS para mejorar el diseño de los botones 🔹
st.sidebar.markdown(
    """
    <style>
    .stButton > button {
        width: 80%;  /* 🔹 Ancho reducido */
        border-radius: 12px;  /* 🔹 Bordes redondeados */
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 8px;
        transition: 0.3s;
        color: white;
        text-align: center;
    }

    /* 🎨 Colores específicos para cada botón */
    .stButton:nth-child(1) button { background-color: #7B1FA2; } /* Morado oscuro */
    .stButton:nth-child(2) button { background-color: #9C27B0; } /* Morado medio */
    .stButton:nth-child(3) button { background-color: #BA68C8; } /* Morado suave */
    .stButton:nth-child(4) button { background-color: #E91E63; } /* Rosa fuerte */
    .stButton:nth-child(5) button { background-color: #F48FB1; } /* Rosa pastel */

    .stButton > button:hover {
        filter: brightness(90%);
    }

    /* 🔹 Negrita y borde para el botón activo */
    .stButton-active > button {
        font-weight: bold;
        border: 2px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Menú lateral con botones funcionales y estilizados
st.sidebar.markdown("### Navegador")

if st.sidebar.button("Inicio"):
    st.session_state.pagina = "Inicio"
if st.sidebar.button("Gestión de corpus"):
    st.session_state.pagina = "Gestión de corpus"
if st.sidebar.button("Extracción terminológica"):
    st.session_state.pagina = "Extracción terminológica"
if st.sidebar.button("Validación de términos"):
    st.session_state.pagina = "Validación de términos"
if st.sidebar.button("Acerca de"):
    st.session_state.pagina = "Acerca de"

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
        - **Extracción terminológica** → Extraer términos mediante métodos como **TF-IDF, POS Tagging y C-Value**.
        - **Validación de términos** → Subir un archivo `.csv` con términos extraídos y validar los candidatos a término.
        
        Usa el menú lateral para navegar entre las distintas funciones.
        """
    )

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# 📌 Menú lateral con botones estilizados
st.sidebar.markdown("### Navegador")

if st.sidebar.button("Inicio"):
    st.session_state.pagina = "Inicio"
if st.sidebar.button("Gestión de corpus"):
    st.session_state.pagina = "Gestión de corpus"
if st.sidebar.button("Visualizador de corpus"):  # Ahora es la funcionalidad 2
    st.session_state.pagina = "Visualizador de corpus"
if st.sidebar.button("Extracción terminológica"):
    st.session_state.pagina = "Extracción terminológica"
if st.sidebar.button("Validación de términos"):
    st.session_state.pagina = "Validación de términos"
if st.sidebar.button("Acerca de"):
    st.session_state.pagina = "Acerca de"

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
