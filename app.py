# Menú lateral para seleccionar la funcionalidad
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
        
        - 📂 **Gestión de corpus** → Subir tus archivos .txt (¡siempre es mejor en UFT-8!) y estructurar tu corpus en un dataset con sus correspondientes metadatos.
        - 🏷️ **Extracción terminológica** → Extraer términos mediante distintos métodos como **TF-IDF, POS Tagging y C-Value** para identificar términos en tu corpus.
        - ✅ **Validación de términos** → Subir un CSV con términos extraídos (¡el que te proporciona esta misma app! y marcar cuáles de ellos son términos reales.  
        
        📌 **Usa el menú lateral para navegar entre las funcionalidades.**
        
        """
    )

    st.image("https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif", width=100)
