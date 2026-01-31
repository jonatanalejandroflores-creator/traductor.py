import streamlit as st
import sys
import io
from types import ModuleType

# --- 1. PARCHE DE COMPATIBILIDAD OBLIGATORIO ---
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

# --- 3. CONFIGURACIÓN ---
st.set_page_config(page_title="Traductor Pro IA", page_icon="🌐", layout="centered")

st.title("🌐 Traductor Pro Multi-Modo")

# Barra lateral para configuración premium
with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("OpenAI API Key:", type="password")
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])

# --- 4. ENTRADA DE DATOS ---
tab1, tab2, tab3 = st.tabs(["⌨️ Texto/Canción", "🎤 Voz", "📸 Imagen (OCR)"])
texto_para_traducir = ""

with tab1:
    texto_manual = st.text_area("Escribe o pega la letra aquí:", height=200)
    if texto_manual:
        texto_para_traducir = texto_manual

with tab2:
    st.write("Graba tu voz:")
    audio_data = mic_recorder(start_prompt="Grabar 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio_data:
        st.audio(audio_data['bytes'])
        st.info("Audio capturado con éxito.")

with tab3:
    archivo_imagen = st.file_uploader("Sube una imagen con texto:", type=['png', 'jpg', 'jpeg'])
    if archivo_imagen:
        img = Image.open(archivo_imagen)
        st.image(img, caption="Imagen cargada", use_container_width=True)
        texto_para_traducir = pytesseract.image_to_string(img)
        st.text_area("Texto detectado:", value=texto_para_traducir)

# --- 5. TRADUCCIÓN Y RESULTADO ---
st.divider()
dest_lang = st.selectbox("Idioma destino:", ["Spanish", "English", "French", "German", "Italian"])
lang_codes = {"Spanish": "es", "English": "en", "French": "fr", "German": "de", "Italian": "it"}

if st.button("TRADUCIR AHORA ✨"):
    if texto_para_traducir:
        try:
            with st.spinner("Procesando..."):
                if motor == "ChatGPT (Premium)" and api_key:
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": f"Traduce al {dest_lang}: {texto_para_traducir}"}]
                    )
                    resultado = response.choices[0].message.content
                else:
                    translator = Translator()
                    res = translator.translate(texto_para_traducir, dest=lang_codes[dest_lang])
                    resultado = res.text

                st.success(f"**Resultado:** {resultado}")
                
                # Audio del resultado
                tts = gTTS(text=resultado, lang=lang_codes[dest_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("No hay texto para traducir.")
