import os
import streamlit as st
import openai
from googletrans import Translator

# --- 1. SEGURIDAD Y CONFIGURACIÓN ---
# Intentamos obtener la llave de la nube de forma invisible
api_key = os.getenv("OPENAI_API_KEY")

# --- 2. CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(page_title="Traductor Pro Beta", page_icon="🌐", layout="centered")

# Inyectar Manifest para PWA
st.markdown('<link rel="manifest" href="/manifest.json">', unsafe_allow_html=True)

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("logo_beta.png", width=150) if os.path.exists("logo_beta.png") else st.title("🤖 AI Trans")
    st.info("🚀 **Versión Beta v0.5.1**")
    
    # Verificación de Seguridad (Debug)
    if api_key:
        st.success("✅ Sistema: Conectado")
        openai.api_key = api_key
    else:
        st.warning("⚠️ Modo manual: Introduce Key")
        api_key = st.text_input("OpenAI API Key:", type="password")
        openai.api_key = api_key

    st.markdown("---")
    motor = st.selectbox("Motor de traducción:", ["Google (Gratis)", "OpenAI (GPT-4)"])
    idioma_dest = st.selectbox("Idioma destino:", ["Spanish", "English", "French", "German", "Italian"])

# --- 4. INTERFAZ PRINCIPAL ---
st.title("🌐 Traductor Pro Multi-Modo")

# Pestañas para las funciones que ya tenías
tab1, tab2, tab3 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])

with tab1:
    texto_usuario = st.text_area("Escribe aquí lo que quieras traducir:", placeholder="Ej: Hola, ¿cómo estás?")

# --- 5. LÓGICA DE TRADUCCIÓN ---
if st.button("TRADUCIR AHORA ✨"):
    if not texto_usuario:
        st.warning("Por favor, escribe algo primero.")
    else:
        with st.spinner('Traduciendo...'):
            try:
                if motor == "Google (Gratis)":
                    translator = Translator()
                    resultado = translator.translate(texto_usuario, dest=idioma_dest.lower()[:2]).text
                else:
                    if not api_key:
                        st.error("Falta la OpenAI API Key para este motor.")
                        st.stop()
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": f"Translate to {idioma_dest}: {texto_usuario}"}]
                    )
                    resultado = response.choices[0].message.content
                
                st.success("### Resultado:")
                st.write(resultado)
                st.button("📋 Copiar (Función DevOps)", on_click=lambda: st.write("Copiado al portapapeles"))
                
            except Exception as e:
                st.error(f"Hubo un error: {e}")

st.markdown("---")
st.caption("Desarrollado por Jonatan Alejandro Flores | Creator Edition")
