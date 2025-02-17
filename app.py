import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos
from acerca_de import acerca_de  # Importamos la sección "Acerca de"

# Inicializar el estado de sesión para la navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

# 🔹 CSS para cambiar los colores de los botones 🔹
st.sidebar.markdown(
    """
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 10px;
        transition: 0.3s;
    }
    
    /* 🎨 Colores para cada botón */
    .stButton:nth-child(1) button { background-color: #4CAF50; color: white; } /* Verde */
    .stButton:nth-child(2) button { background-color: #2196F3; color: white; } /* Azul */
    .stButton:nth-child(3) button { background-color: #FF9800; color: white; } /* Naranja */
    .stButton:nth-child(4) button { background-color: #F44336; color: white; } /* Rojo */
    .stButton:nth-child(5) button { background-color: #9C27B0; color: white; } /* Morado */

    .stButton > button:hover {
        filter: brightness(90%);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------
# Funcionalidad 0: Pantalla de Inicio
# ------------------------------
if st.session_state.pagina == "Inicio":
    st.title("🤖 TermoLing, una estación de trabajo terminográfico")
    st.markdown(
        """
        👋 ¡Hola! Esta es una aplicación creada para ayudarte en la gestión y minería de textos, especialmente diseñada para asistirte en el trabajo terminográfico.
        
        🔍 **¿Qué puedes hacer aquí?**
        
        - 📂 **Gestión de corpus** → Subir archivos `.txt` (¡siempre es mejor si está codificado en UTF-8!) y estructurar un corpus con metadatos.
        - 📊 **Extracción terminológica** → Extraer términos mediante métodos como **TF-IDF, POS Tagging y C-Value**.
        - ✅ **Validación de términos** → Subir un archivo `.csv` con términos extraídos (¡el mismo que te genera esta app!) y validar los candidatos a término.
        
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

# ------------------------------
# Funcionalidad 4: Acerca de
# ------------------------------
elif st.session_state.pagina == "Acerca de":
    acerca_de()
