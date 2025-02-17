import streamlit as st

def acerca_de():
    st.title("📌 Acerca de esta aplicación")
    
    st.markdown(
        """
        ### 👩‍💻 Sobre mí
        
        ¡Hola! Soy **Isabel Moyano Moreno**, investigadora predoctoral en **Lingüística Computacional** y miembro del grupo de investigación **Semaínein**.
        
        Mis líneas de investigación principales son:
        - **Terminología computacional y extracción automática de términos**
        - **Lingüística de corpus**
        - **Estilometría**
        
        ### 🔍 Sobre esta aplicación
        
        Creé esta app para facilitar la **gestión y análisis de corpus lingüísticos** con fines terminológicos a partir de la implementación de distintas herramientas de **procesamiento del lenguaje natural (PLN)**.
        
        Funcionalidades principales:
        - **Gestión de corpus** → Subir archivos `.txt` y estructurar un corpus con metadatos.
        - **Extracción terminológica** → Identificar términos clave en textos mediante métodos computacionales.
        - **Validación de términos** → Marcar términos extraídos como válidos o no.
                
        ### 📬 Contacto
        Si te interesa mi trabajo, puedes encontrarme por aquí:
        - 🔗 [ORCID](https://orcid.org/0000-0003-4284-8897)
        - 🔗 [LinkedIn](https://www.linkedin.com/in/isabel-moyano-moreno-62619a1bb/)
        - 🔗 [Twitter/X](https://twitter.com/issyinthesky)
        
        """
    )
