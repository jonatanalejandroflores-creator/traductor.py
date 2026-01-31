import streamlit as st
import sys
import io
from types import ModuleType

# --- 1. PARCHE CGI PARA PYTHON 3.13 ---
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

with st.sidebar:
    st.header("Configuración")
    api_key = st.text_input("OpenAI API Key:", type="password")
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])

# --- 4. INTERFAZ ---
tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])
texto_para_traducir = ""

with tab1:
    t_manual = st.text_area("Escribe aquí:", height=150, key="t_manual")
    if t_manual: texto_para_traducir = t_manual

with tab2:
    st.write("Graba tu voz:")
    audio = mic_recorder(start_prompt="Grabar 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio:
        st.audio(audio['bytes'])
        st.info("Audio listo.")

with tab3:
    img_file = st.file_uploader("Sube imagen:", type=['png', 'jpg', 'jpeg'])
    if img_file:
        img = Image.open(img_file)
        st.image(img, use_container_width=True)
        # Extraer texto de la imagen
        detectado = pytesseract.image_to_string(img)
        st.text_area("Texto detectado:", value=detectado, height=150)
        texto_para_traducir = detectado

# --- 5. LÓGICA DE TRADUCCIÓN (BLINDADA) ---
st.divider()
dest_lang = st.selectbox("Idioma destino:", ["Spanish", "English", "French", "German"])
lang_codes = {"Spanish": "es", "English": "en", "French": "fr", "German": "de"}

if st.button("TRADUCIR AHORA ✨"):
    if texto_para_traducir and texto_para_traducir.strip():
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
                    # USAMOS ESTA FORMA PARA EVITAR EL ERROR DE UNPACK
                    gt = Translator()
                    # Realizamos la traducción y guardamos el objeto completo
                    obj_traduccion = gt.translate(texto_para_traducir, dest=lang_codes[dest_lang])
                    # Extraemos solo el texto del objeto
                    resultado_final = obj_traduccion.text

                # Mostrar resultado
                st.success("**Traducción:**")
                st.write(resultado_final)
                
                # Generar audio
                tts = gTTS(text=resultado_final, lang=lang_codes[dest_lang])
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                st.audio(audio_fp)

        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("⚠️ No se encontró texto para traducir.")
