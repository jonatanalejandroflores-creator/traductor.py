import streamlit as st
import sys
import io
from types import ModuleType
from PIL import Image
import pytesseract
import openai
from deep_translator import GoogleTranslator
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# --- PARCHE PARA PYTHON 3.13 ---
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

# --- CONFIGURACIÓN ---
import os
# ... tus otros imports ...

# Intentar obtener la clave desde el sistema (Nube o .env)
api_key = os.getenv("OPENAI_API_KEY")

# Si no existe en el sistema, mostrar el input (como respaldo)
if not api_key:
    with st.sidebar:
        api_key = st.text_input("OpenAI API Key:", type="password")

# Verificamos si el archivo existe para evitar errores
LOGO_PATH = "logo_beta.png" if os.path.exists("logo_beta.png") else None

st.set_page_config(
    page_title="Traductor Creator Edition Beta",
    page_icon=LOGO_PATH,
    layout="centered"
)
# Inyectar el manifest para que sea una PWA
st.markdown(
    """
    <link rel="manifest" href="https://raw.githubusercontent.com/jonatanalejandroflores-creator/traductor.ia/main/manifest.json">
    """,
    unsafe_allow_html=True
)
# --- FORZAR ICONO EN MÓVILES (Fuera del sidebar para mejor carga) ---
st.markdown(
    """
    <link rel="apple-touch-icon" sizes="180x180" href="https://raw.githubusercontent.com/jonatanalejandroflores-creator/traductor.ia/main/logo_beta.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://raw.githubusercontent.com/jonatanalejandroflores-creator/traductor.ia/main/logo_beta.png">
    """, 
    unsafe_allow_html=True
)

with st.sidebar:
    if LOGO_PATH:
        try:
            st.image(LOGO_PATH, width=150)
        except Exception:
            st.write("🌐 **Traductor Creator Edition**")
    
    st.info("🚀 **Versión Beta v0.5.1 - Token Secure**")
    st.markdown("<h3 style='text-align: center;'>Configuración</h3>", unsafe_allow_html=True)
    
    api_key = st.text_input("OpenAI API Key:", type="password")
    # ... resto de tu código
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])
    
    st.divider()
    st.info("🚀 **Versión Beta v0.5**")
    st.caption("👤 **Creator Edition**")
    st.caption("Desarrollado por Jonatan Alejandro Flores")

# --- CUERPO PRINCIPAL ---
st.title("🌐 Traductor Pro Multi-Modo")
st.write("---")

tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])
texto_para_traducir = ""

with tab1:
    t_manual = st.text_area("Escribe aquí:", height=150, key="manual_text")
    if t_manual: texto_para_traducir = t_manual

with tab2:
    audio = mic_recorder(start_prompt="Grabar 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio:
        st.audio(audio['bytes'])
        st.info("Audio capturado.")

with tab3:
    img_file = st.file_uploader("Sube imagen:", type=['png', 'jpg', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        detectado = pytesseract.image_to_string(img)
        st.text_area("Texto detectado:", value=detectado, height=150)
        texto_para_traducir = detectado

# --- TRADUCCIÓN (ESTA PARTE DEBE ESTAR BIEN ALINEADA) ---
st.divider()
dest_lang = st.selectbox("Idioma destino:", ["Spanish", "English", "French", "German"])
lang_codes = {"Spanish": "es", "English": "en", "French": "fr", "German": "de"}

if st.button("TRADUCIR AHORA ✨"):
    if texto_para_traducir.strip():
        try:
            with st.spinner("Traduciendo..."):
                if motor == "ChatGPT (Premium)" and api_key:
                    client = openai.OpenAI(api_key=api_key)
                    res = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": f"Traduce al {dest_lang}: {texto_para_traducir}"}]
                    )
                    resultado_final = res.choices[0].message.content
                else:
                    # Motor Google estable
                    target = lang_codes[dest_lang]
                    resultado_final = GoogleTranslator(source='auto', target=target).translate(texto_para_traducir)

                st.success("**Resultado:**")
                st.write(resultado_final)
                
                tts = gTTS(text=resultado_final, lang=lang_codes[dest_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("⚠️ No hay texto para traducir.")
