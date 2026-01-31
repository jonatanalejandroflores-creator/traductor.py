import streamlit as st
import sys
import io
from types import ModuleType

# --- 1. PARCHE DE COMPATIBILIDAD ---
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

# --- 2. IMPORTACIONES ---
from PIL import Image
import pytesseract
import openai
from googletrans import Translator
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

# --- 3. INTERFAZ ---
st.set_page_config(page_title="Traductor Pro IA", page_icon="🌐")
st.title("🌐 Traductor Pro Multi-Modo")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("OpenAI API Key:", type="password")
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])

tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])
texto_final = ""

with tab1:
    t_manual = st.text_area("Escribe aquí:", key="t_manual")
    if t_manual: texto_final = t_manual

with tab2:
    audio = mic_recorder(start_prompt="Grabar 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio: st.audio(audio['bytes'])

with tab3:
    img_file = st.file_uploader("Sube imagen:", type=['png', 'jpg', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        texto_final = pytesseract.image_to_string(img)
        st.text_area("Detectado:", value=texto_final)

# --- 4. TRADUCCIÓN CORREGIDA ---
st.divider()
idioma = st.selectbox("Destino:", ["Spanish", "English", "French", "German"])
codigos = {"Spanish": "es", "English": "en", "French": "fr", "German": "de"}

if st.button("TRADUCIR AHORA ✨"):
    if texto_final.strip():
        try:
            with st.spinner("Traduciendo..."):
                if motor == "ChatGPT (Premium)" and api_key:
                    client = openai.OpenAI(api_key=api_key)
                    res = client.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": f"Translate to {idioma}: {texto_final}"}]
                    )
                    resultado = res.choices[0].message.content
                else:
                    # CAMBIO CLAVE: Manejo simple del objeto de traducción
                    gt = Translator()
                    traduccion_obj = gt.translate(texto_final, dest=codigos[idioma])
                    resultado = traduccion_obj.text # Acceso directo a la propiedad .text

                st.success(f"**Resultado:** {resultado}")
                
                # Audio
                tts = gTTS(text=resultado, lang=codigos[idioma])
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp)
        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe algo o sube una imagen primero.")
