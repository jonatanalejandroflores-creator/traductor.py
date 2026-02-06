import streamlit as st
import numpy as np
from PIL import Image
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io
import pytesseract # Asegúrate de tenerlo en requirements.txt

# 1. Configuración de página
st.set_page_config(page_title="Traductor Pro Multi-Modo", layout="wide")

# 2. Lógica de Idiomas
@st.cache_data
def obtener_idiomas():
    try:
        dict_soporte = GoogleTranslator().get_supported_languages(as_dict=True)
        return {name.title(): code for name, code in dict_soporte.items()}
    except:
        return {"Spanish": "es", "English": "en", "French": "fr"}

idiomas_dict = obtener_idiomas()
lista_nombres = sorted(list(idiomas_dict.keys()))

# 3. Barra Lateral
st.sidebar.image("logo_beta.png", width=150)
st.sidebar.title("Configuración")
openai_key = st.sidebar.text_input("OpenAI API Key:", type="password")
motor = st.sidebar.selectbox("Motor:", ["Google (Gratis)", "OpenAI (GPT-4)"])
st.sidebar.markdown("---")
st.sidebar.info("Versión Beta v0.7 - OCR & TTS")
st.sidebar.info("Desarrollado por Jonatan Alejandro Flores")

st.title("🌐 Traductor Pro Multi-Modo")

# --- SECCIÓN 1: EL TRADUCTOR TRIPLE ---
tabs = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])

with tabs[0]: # Pestaña de Texto + Salida de Audio
    texto_origen = st.text_area("Escribe aquí para traducir:", height=150, key="txt_area")
    idioma_nombre = st.selectbox("Idioma destino:", lista_nombres, index=lista_nombres.index("English") if "English" in lista_nombres else 0, key="sel_txt")
    idioma_cod = idiomas_dict[idioma_nombre]
    
    if st.button("TRADUCIR TEXTO ✨"):
        if texto_origen:
            res = GoogleTranslator(source='auto', target=idioma_cod).translate(texto_origen)
            st.success(f"**Traducción:** {res}")
            try:
                tts = gTTS(text=res, lang=idioma_cod)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                st.audio(fp, format='audio/mp3')
            except:
                st.warning("Audio no disponible para este idioma.")

with tabs[1]: # Pestaña de Voz
    st.subheader("Entrada por Voz")
    st.info("Graba tu mensaje para procesarlo.")
    audio_input = mic_recorder(start_prompt="Grabar Voz 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio_input:
        st.audio(audio_input['bytes'])

with tabs[2]: # Pestaña de Imagen + OCR
    st.subheader("Traducción desde Imagen")
    archivo_imagen = st.file_uploader("Sube una foto clara con texto:", type=['jpg', 'png', 'jpeg'])
    
    if archivo_imagen:
        img = Image.open(archivo_imagen)
        st.image(img, caption="Imagen cargada", use_container_width=True)
        idioma_img = st.selectbox("Traducir imagen a:", lista_nombres, key="sel_img")
        
        if st.button("EXTRAER Y TRADUCIR 🔍"):
            with st.spinner("Procesando imagen..."):
                try:
                    texto_extraido = pytesseract.image_to_string(img)
                    if texto_extraido.strip():
                        st.info(f"**Texto detectado:** {texto_extraido[:200]}...")
                        traduccion_img = GoogleTranslator(source='auto', target=idiomas_dict[idioma_img]).translate(texto_extraido)
                        st.success(f"**Traducción:** {traduccion_img}")
                    else:
                        st.error("No se detectó texto. Prueba con otra imagen.")
                except Exception as e:
                    st.error("Error: Tesseract OCR no está configurado en el servidor.")

# --- SECCIÓN 2: ÁLGEBRA (NumPy) ---
st.markdown("---")
st.header("📐 Laboratorio de Álgebra (NumPy)")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Vector A")
    ax, ay, az = st.number_input("Ax", value=3.0), st.number_input("Ay", value=-2.0), st.number_input("Az", value=1.0)
with col2:
    st.subheader("Vector B")
    bx, by, bz = st.number_input("Bx", value=0.0), st.number_input("By", value=4.0), st.number_input("Bz", value=-3.0)

if st.button("CALCULAR OPERACIONES 🧮"):
    vec_a, vec_b = np.array([ax, ay, az]), np.array([bx, by, bz])
    st.write(f"🔹 **Producto Punto:** {np.dot(vec_a, vec_b)}")
    st.write(f"🔹 **Producto Vectorial:** {np.cross(vec_a, vec_b).tolist()}")
