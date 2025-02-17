import streamlit as st
import pandas as pd

def validacion_terminos():
    st.title("✅ Validación de términos extraídos")

    st.markdown(
        """
        🔍 **Instrucciones para la validación de términos**
        
        📎 **Sube un archivo CSV con los términos extraídos**.
        """
    )

    uploaded_file = st.file_uploader("📎 Sube tu archivo CSV aquí", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "Términos extraídos" not in df.columns:
            st.error("⚠️ El archivo debe contener una columna llamada 'Términos extraídos'.")
        else:
            if "Es término" not in df.columns:
                df["Es término"] = False  

            st.subheader("🔍 Revisión de términos")
            df_editable = st.data_editor(df, num_rows="dynamic", key="term_editor")

            df_validated = df_editable[df_editable["Es término"] == True][["Términos extraídos"]]

            csv_data = df_validated.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descargar CSV", data=csv_data, file_name="terminos_validados.csv", mime="text/csv")
