import streamlit as st
import pandas as pd 
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos

# Menú lateral para elegir entre funciones
opcion = st.sidebar.radio("", ["Inicio", "Gestión de corpus", "Extracción terminológica", "Validación de términos"])

# ------------------------------
# Funcionalidad 0: Pantalla de Inicio
# ------------------------------
if opcion == "Inicio":
    st.title("📌 App para el trabajo terminográfico")

    st.markdown(
        """
        👋 ¡Hola! Esta es una aplicación diseñada para ayudarte en la gestión y minería de textos, especialmente diseñada para asistirte en el trabajo terminográfico.
        
        🔍 **¿Qué puedes hacer aquí?**
        
        - 📂 **Gestión de corpus** → Subir tus archivos .txt (¡siempre es mejor en UTF-8!) y estructurar tu corpus en un dataset con sus correspondientes metadatos.
        - 🏷️ **Extracción terminológica** → Extraer términos mediante distintos métodos como **TF-IDF, POS Tagging y C-Value** para identificar términos en tu corpus.
        - ✅ **Validación de términos** → Subir un CSV con términos extraídos (¡el que te proporciona esta misma app!) y marcar cuáles de ellos son términos reales.  
        
        📌 **Usa el menú lateral para navegar entre las distintas funciones. ¡Espero que te sirva!**
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
