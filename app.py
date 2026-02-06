import streamlit as st
import numpy as np
from PIL import Image
from deep_translator import GoogleTranslator
from streamlit_mic_recorder import mic_recorder
from gtts import gTTS
import io

# 1. Configuración de página
st.set_page_config(page_title="Traductor Pro Multi-Modo", layout="wide")

# 2. Lógica de Idiomas (+100 automáticos)
@st.cache_data
def obtener_idiomas():
    try:
        dict_soporte = GoogleTranslator().get_supported_languages(as_dict=True)
        return {name.title(): code for name, code in dict_soporte.items()}
    except:
        return {"Spanish": "es", "English": "en", "French": "fr", "Italian": "it"}

idiomas_dict = obtener_idiomas()
lista_nombres = sorted(list(idiomas_dict.keys()))

# 3. Barra Lateral (Tu diseño original)
st.sidebar.image("logo_beta.png", width=150)
st.sidebar.title("Configuración")
openai_key = st.sidebar.text_input("OpenAI API Key:", type="password")
motor = st.sidebar.selectbox("Motor:", ["Google (Gratis)", "OpenAI (GPT-4)"])
st.sidebar.markdown("---")
st.sidebar.info("Versión Beta v0.6")
st.sidebar.info("Desarrollado por Jonatan Alejandro Flores")

st.title("🌐 Traductor Pro Multi-Modo")

# --- SECCIÓN 1: EL TRADUCTOR TRIPLE ---
tabs = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])

with tabs[0]: # Pestaña de Texto + AUDIO
    texto_origen = st.text_area("Escribe aquí:", height=150, key="txt_area")
    idioma_nombre = st.selectbox("Idioma destino:", lista_nombres, index=lista_nombres.index("English") if "English" in lista_nombres else 0)
    idioma_cod = idiomas_dict[idioma_nombre]
    
    if st.button("TRADUCIR AHORA ✨"):
        if texto_origen:
            # Traducción
            res = GoogleTranslator(source='auto', target=idioma_cod).translate(texto_origen)
            st.success(f"**Traducción ({idioma_nombre}):** {res}")
            
            # Generación de Audio (TTS)
            try:
                tts = gTTS(text=res, lang=idioma_cod)
                audio_fp = io.BytesIO()
                tts.write_to_fp(audio_fp)
                st.audio(audio_fp, format='audio/mp3')
            except Exception as e:
                st.warning("El audio no está disponible para este idioma.")

with tabs[1]: # Pestaña de Voz (Entrada)
    st.subheader("Entrada por Voz")
    st.info("Graba tu voz para traducirla (Requiere configuración de SpeechRecognition)")
    audio_input = mic_recorder(start_prompt="Grabar Voz 🎙️", stop_prompt="Detener 🛑", key='recorder')
    if audio_input:
        st.audio(audio_input['bytes'])

with tabs[2]: # Pestaña de Imagen (OCR)
    st.subheader("Traducción desde Imagen")
    archivo_imagen = st.file_uploader("Sube una foto:", type=['jpg', 'png', 'jpeg'])
    if archivo_imagen:
        img = Image.open(archivo_imagen)
        st.image(img, use_container_width=True)
        st.button("EXTRAER TEXTO 🔍")

# --- SECCIÓN 2: ÁLGEBRA (NumPy) ---
st.markdown("---")
st.header("📐 Laboratorio de Álgebra (NumPy)")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Vector A")
    ax = st.number_input("Ax", value=3.0)
    ay = st.number_input("Ay", value=-2.0)
    az = st.number_input("Az", value=1.0)
with col2:
    st.subheader("Vector B")
    bx = st.number_input("Bx", value=0.0)
    by = st.number_input("By", value=4.0)
    bz = st.number_input("Bz", value=-3.0)

if st.button("CALCULAR OPERACIONES 🧮"):
    vec_a = np.array([ax, ay, az])
    vec_b = np.array([bx, by, bz])
    st.divider()
    st.write(f"🔹 **Producto Punto:** {np.dot(vec_a, vec_b)}")
    st.write(rf"🔹 **Producto Vectorial:** {np.cross(vec_a, vec_b).tolist()}")
