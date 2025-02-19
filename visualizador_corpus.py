def dividir_texto(texto, tamano_maximo=1_000_000):
    """Divide el texto en fragmentos más pequeños para evitar el límite de spaCy."""
    return [texto[i : i + tamano_maximo] for i in range(0, len(texto), tamano_maximo)]

def calcular_estadisticas(texto):
    """Calcula estadísticas básicas del corpus en fragmentos."""
    if not isinstance(texto, str) or not texto.strip():
        return None  

    fragmentos = dividir_texto(texto)
    total_tokens, total_palabras, total_tipos = 0, 0, set()
    total_palabras_contenido = set()

    for fragmento in fragmentos:
        doc = nlp(fragmento)
        tokens = [token.text for token in doc]
        palabras = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stop_words]
        total_tokens += len(tokens)
        total_palabras += len(palabras)
        total_tipos.update(palabras)
        total_palabras_contenido.update([token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]])

    return {
        "Total de tokens": total_tokens,
        "Total de palabras": total_palabras,
        "Palabras únicas (Type)": len(total_tipos),
        "Type-Token Ratio (TTR)": len(total_tipos) / total_tokens if total_tokens > 0 else 0,
        "Densidad léxica": len(total_palabras_contenido) / total_tokens if total_tokens > 0 else 0
    }

def generar_nube_palabras(texto):
    """Genera una nube de palabras sin sobrepasar el límite de spaCy."""
    if not isinstance(texto, str) or not texto.strip():
        st.warning("⚠️ No hay texto válido para generar una nube de palabras.")
        return None

    fragmentos = dividir_texto(texto)
    palabras_totales = []

    for fragmento in fragmentos:
        doc = nlp(fragmento)
        palabras = [token.text.lower() for token in doc if token.is_alpha and token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"] and token.text.lower() not in stop_words]
        palabras_totales.extend(palabras)

    if not palabras_totales:
        st.warning("⚠️ No hay suficientes palabras de contenido para generar una nube de palabras.")
        return None

    frecuencia = Counter(palabras_totales)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(frecuencia)

    # Guardamos la imagen en memoria para permitir la descarga
    buffer = BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    
    return buffer
