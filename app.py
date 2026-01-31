import streamlit as st
import sys
import io
from types import ModuleType

# --- 1. PARCHE DE COMPATIBILIDAD (Para que no vuelva el error CGI) ---
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

# --- 4. INTERFAZ (TABS) ---
tab1, tab2, tab3 = st.tabs(["⌨️ Texto/Canción", "🎤 Voz", "📸 Imagen (OCR)"])
texto_para_traducir = ""

with tab1:
    texto_manual = st.text_area("Escribe o pega aquí:", height=200)
    if texto_manual:
        texto_para_traducir = texto_manual

with tab2:
    st.write("Graba tu voz:")
    audio_data = mic_recorder(start_prompt="Grabar 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio_data:
        st.audio(audio_data['bytes'])
        st.info("Audio capturado.")

with tab3:
    archivo_imagen = st.file_uploader("Sube una imagen:", type=['png', 'jpg', 'jpeg'])
    if archivo_imagen:
        img = Image.open(archivo_imagen)
        st.image(img, caption="Imagen cargada", use_container_width=True)
        # Extraer texto de la imagen (OCR)
        texto_para_traducir = pytesseract.image_to_string(img)
        st.text_area("Texto detectado:", value=texto_para_traducir)

# --- 5. TU BLOQUE DE TRADUCCIÓN (EL QUE ARREGLASTE) ---
st.divider()
dest_lang = st.selectbox("Idioma destino:", ["Spanish", "English", "French", "German"])
lang_codes = {"Spanish": "es", "English": "en", "French": "fr", "German": "de"}

if st.button("TRADUCIR AHORA ✨"):
    # .strip() asegura que no enviemos texto vacío al traductor
    texto_limpio = texto_para_traducir.strip()
    
    if texto_limpio:
        try:
            with st.spinner("Traduciendo..."):
                if motor == "ChatGPT (Premium)" and api_key:
                    client = openai.OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": f"Traduce al {dest_lang}: {texto_limpio}"}]
                    )
                    resultado_final = response.choices[0].message.content
                else:
                    # USAR ESTA FORMA PARA EVITAR EL ERROR DE 'UNPACK'
                    translator = Translator()
                    # Solo pedimos la traducción al idioma destino
                    traduccion_objeto = translator.translate(texto_limpio, dest=lang_codes[dest_lang])
                    resultado_final = traduccion_objeto.text

                # --- MOSTRAR RESULTADO ---
                st.success("**Traducción:**")
                st.write(resultado_final)
                
                # Generar el audio
                tts = gTTS(text=resultado_final, lang=lang_codes[dest_lang])
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp)

        except Exception as e:
            # Esto atrapará el error y te dirá exactamente qué pasó sin romper la app
            st.error(f"Hubo un problema técnico: {e}")
    else:
        st.warning("⚠️ Primero detecta o escribe algún texto para traducir.")
