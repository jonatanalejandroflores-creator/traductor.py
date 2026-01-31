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
st.set_page_config(page_title="Traductor Pro IA", page_icon="🌐")
st.title("🌐 Traductor Pro Multi-Modo")

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("OpenAI API Key:", type="password")
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])

tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])
texto_para_traducir = ""

with tab1:
    t_manual = st.text_area("Escribe aquí:", height=150, key="manual")
    if t_manual: texto_para_traducir = t_manual

with tab2:
    st.write("Graba tu voz:")
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

# --- TRADUCCIÓN ---
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
                    # Usamos Deep Translator (Sintaxis ultra simple)
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
