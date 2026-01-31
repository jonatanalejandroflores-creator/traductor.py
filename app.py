import streamlit as st
import sys
from types import ModuleType

# --- SUPER PARCHE DE COMPATIBILIDAD (Arregla el error de 'cgi') ---
try:
    import cgi
except ImportError:
    cgi = ModuleType('cgi')
    sys.modules['cgi'] = cgi

if not hasattr(cgi, 'parse_header'):
    def parse_header(line):
        import email.utils
        return email.utils.decode_params('; ' + line)[0]
    cgi.parse_header = parse_header
# -----------------------------------------------------------------

from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Traductor Pro IA",
    page_icon="🌐",
    layout="centered"
)

st.title("🎵 Traductor de Canciones AI")
st.markdown("Identifica el idioma automáticamente y traduce al español.")

# Área de texto para la letra
letra_input = st.text_area("Pega la letra de tu canción aquí:", height=300)

if st.button("Traducir Ahora"):
    if letra_input.strip():
        translator = Translator()
        with st.spinner('Procesando traducción...'):
            try:
                # Traducción (Corregido el error de 'dest')
                resultado = translator.translate(letra_input, src='auto', dest='es')

                # Mostrar resultados en columnas
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Origen ({resultado.src.upper()})")
                    st.info(letra_input)
                with col2:
                    st.subheader("Traducción (ES)")
                    st.success(resultado.text)

            except Exception as e:
                st.error(f"Error técnico: {e}")
    else:
        st.warning("Por favor, ingresa algún texto.")

st.sidebar.info("Demo Técnica - Técnico Informático")

