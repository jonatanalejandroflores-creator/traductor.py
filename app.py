import streamlit as st
import sys
from types import ModuleType

# --- 1. SUPER PARCHE DE COMPATIBILIDAD (Obligatorio para Python 3.13) ---
# Este bloque "engaña" a la app creando un módulo cgi falso para que no de error
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
# -----------------------------------------------------------------------

# --- 2. AHORA SÍ PODEMOS IMPORTAR EL TRADUCTOR ---
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Traductor Pro IA",
    page_icon="🌐",
    layout="centered"
)

st.title("🎵 Traductor de Canciones AI")
st.markdown("Identifica el idioma automáticamente y traduce al español.")

# Área de texto
letra_input = st.text_area("Pega la letra de tu canción aquí:", height=300)

if st.button("Traducir Ahora"):
    if letra_input.strip():
        translator = Translator()
        with st.spinner('Procesando traducción...'):
            try:
                # Traducción al español
                resultado = translator.translate(letra_input, src='auto', dest='es')

                # Diseño de resultados
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader(f"Origen ({resultado.src.upper()})")
                    st.info(letra_input)
                with col2:
                    st.subheader("Traducción (ES)")
                    st.success(resultado.text)

            except Exception as e:
                st.error(f"Error en la traducción: {e}")
    else:
        st.warning("Por favor, escribe algo antes de traducir.")

st.sidebar.info("Demo Técnica - Técnico Informático")
