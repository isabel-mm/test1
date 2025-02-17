import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos
from acerca_de import acerca_de  # Importamos la sección "Acerca de"

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# 🔹 CSS para personalizar los botones y el estado activo 🔹
st.sidebar.markdown(
    """
    <style>
    .sidebar-buttons {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .sidebar-buttons button {
        width: 80%;  /* 🔹 Reducimos el ancho de los botones */
        border-radius: 8px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 8px;
        margin-bottom: 5px;
        transition: 0.3s;
        color: white;
        text-align: center;
    }

    /* 🎨 Colores específicos para cada botón */
    .sidebar-buttons button:nth-child(1) { background-color: #7B1FA2; } /* Morado oscuro */
    .sidebar-buttons button:nth-child(2) { background-color: #9C27B0; } /* Morado medio */
    .sidebar-buttons button:nth-child(3) { background-color: #BA68C8; } /* Morado suave */
    .sidebar-buttons button:nth-child(4) { background-color: #E91E63; } /* Rosa fuerte */
    .sidebar-buttons button:nth-child(5) { background-color: #F48FB1; } /* Rosa pastel */

    .sidebar-buttons button:hover {
        filter: brightness(85%);
    }

    /* 🔹 Negrita y borde para el botón activo */
    .stButton-active button {
        font-weight: 900;
        border: 2px solid white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Menú lateral con botones de colores y ancho reducido
st.sidebar.markdown('<div class="sidebar-buttons">', unsafe_allow_html=True)

def styled_button(label, page):
    """Crea un botón estilizado y cambia la página activa."""
    if st.session_state.pagina == page:
        st.markdown('<div class="stButton-active">', unsafe_allow_html=True)
        clicked = st.sidebar.button(label)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        clicked = st.sidebar.button(label)
    if clicked:
        st.session_state.pagina = page

# Agregar botones con estilos personalizados
styled_button("Inicio", "Inicio")
styled_button("Gestión de corpus", "Gestión de corpus")
styled_button("Extracción terminológica", "Extracción terminológica")
styled_button("Validación de términos", "Validación de términos")
styled_button("Acerca de", "Acerca de")

st.sidebar.markdown('</div>', unsafe_allow_html=True)

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

# ------------------------------
# Funcionalidad 4: Acerca de
# ------------------------------
elif st.session_state.pagina == "Acerca de":
    acerca_de()
