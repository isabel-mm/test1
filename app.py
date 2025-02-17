import streamlit as st
from gestion_corpus import gestion_corpus
from extraccion_terminos import extraccion_terminologica
from validacion_terminos import validacion_terminos

# Menú lateral para seleccionar la funcionalidad
st.sidebar.title("Menú de funciones")
opcion = st.sidebar.radio("", ["Gestión de corpus", "Extracción terminológica", "Validación de términos"])

# Ejecutar la funcionalidad seleccionada
if opcion == "Gestión de corpus":
    gestion_corpus()
elif opcion == "Extracción terminológica":
    extraccion_terminologica()
elif opcion == "Validación de términos":
    validacion_terminos()
