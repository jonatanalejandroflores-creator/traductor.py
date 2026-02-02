import os
import streamlit as st
import openai
from googletrans import Translator

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
# Intentamos obtener la clave real de la nube
api_key_env = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Traductor Pro v1.0", page_icon="🌐", layout="centered")

# --- 2. BARRA LATERAL (LIMPIEZA TOTAL) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3858/3858902.png", width=80)
    st.title("Configuración")
    st.info("🚀 **Versión Final v1.0**")
    
    # Si la clave de la nube es real (empieza con sk-), no pedimos nada
    if api_key_env and api_key_env.startswith("sk-"):
        st.success("✅ Conexión Premium Activa")
        api_key = api_key_env
    else:
        st.warning("⚠️ Usando Modo Gratuito")
        api_key = st.text_input("Introduce OpenAI Key real:", type="password", help="Para activar Voz y GPT-4")
    
    openai.api_key = api_key
    motor = st.selectbox("Motor de IA:", ["Google (Gratis)", "ChatGPT (Premium)"])
    st.markdown("---")
    st.caption("👤 Desarrollado por Jonatan Alejandro Flores")

# --- 3. CUERPO PRINCIPAL ---
st.title("🌐 Traductor Pro Multi-Modo")

if "texto_capturado" not in st.session_state:
    st.session_state.texto_capturado = ""

tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])

with tab1:
    texto_final = st.text_area("Tu mensaje:", value=st.session_state.texto_capturado, height=150)

with tab2:
    st.write("### 🎙️ Grabadora de Voz")
    audio_data = st.audio_input("Presiona para hablar")
    
    if audio_data and st.button("Transcribir Audio 🤖"):
        if not api_key.startswith("sk-"):
            st.error("Se requiere una API Key real para procesar voz.")
        else:
            try:
                with st.spinner("Procesando..."):
                    # Usamos el buffer directo para evitar errores de archivo en el servidor
                    audio_bytes = audio_data.read()
                    # Le damos un nombre virtual para OpenAI
                    audio_data.name = "audio.wav" 
                    
                    transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_data)
                    st.session_state.texto_capturado = transcript.text
                    st.success("¡Texto capturado!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error técnico: {e}")

# --- 4. ACCIÓN DE TRADUCCIÓN ---
idioma = st.selectbox("Traducir al:", ["Spanish", "English", "French", "German"])

if st.button("TRADUCIR AHORA ✨"):
    if not texto_final:
        st.warning("Escribe o graba algo primero.")
    else:
        try:
            with st.spinner('Traduciendo...'):
                if motor == "Google (Gratis)":
                    res = Translator().translate(texto_final, dest=idioma[:2].lower()).text
                else:
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": f"Translate to {idioma}: {texto_final}"}]
                    )
                    res = response.choices[0].message.content
                
                st.success(f"### Resultado:\n{res}")
                # El reproductor de audio que viste en tu captura:
                st.audio(f"https://translate.google.com/translate_tts?ie=UTF-8&q={res.replace(' ', '%20')}&tl={idioma[:2].lower()}&client=tw-ob")
        except Exception as e:
            st.error("Error en la traducción. Revisa tu clave si usas motor Premium.")
