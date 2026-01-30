import streamlit as st
from googletrans import Translator

# Configuración de la página
st.set_page_config(page_title="Music Translator Demo", page_icon="🎵")

st.title("🎵 Traductor de Canciones AI")
st.markdown("Identifica el idioma automáticamente y traduce al español.")

# Área de texto para la letra
letra_input = st.text_area("Pega la letra de tu canción aquí:", height=300)

if st.button("Traducir Ahora"):
    if letra_input.strip():
        translator = Translator()
        with st.spinner('Procesando traducción...'):
            try:
                # Traducción
                resultado = translator.translate(letra_input, src='auto', dest='es')
                
                # Mostrar resultados en columnas
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Origen ({resultado.src})")
                    st.info(letra_input)
                with col2:
                    st.subheader("Traducción (ES)")
                    st.success(resultado.text)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, ingresa algún texto.")

st.sidebar.info("Demo Técnica - Técnico Informático")

