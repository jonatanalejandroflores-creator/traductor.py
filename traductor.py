import os
import streamlit as st
import openai
from googletrans import Translator

# --- CONFIGURACIÓN DE SEGURIDAD ---
api_key_env = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="AI Trans Pro v1.1", page_icon="🌐")

# --- INICIALIZAR LA "CAJA DE MEMORIA" (HISTORIAL) ---
if "historial" not in st.session_state:
    st.session_state.historial = []

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3858/3858902.png", width=80)
    st.title("Configuración")
    st.info("🚀 **Fase 2: Memoria Activa**")
    
    if api_key_env and api_key_env.startswith("sk-"):
        st.success("✅ Conexión Premium")
        api_key = api_key_env
    else:
        api_key = st.text_input("API Key:", type="password")
    
    openai.api_key = api_key
    motor = st.selectbox("Motor:", ["Google (Gratis)", "ChatGPT (Premium)"])

# --- CUERPO PRINCIPAL ---
st.title("🌐 AI Trans Pro")

tab1, tab2, tab3, tab4 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen", "📜 Historial"])

with tab1:
    texto_input = st.text_area("Escribe aquí:", height=100)

with tab2:
    st.write("### Grabadora")
    audio_data = st.audio_input("Habla ahora")

# --- LÓGICA DE TRADUCCIÓN ---
idioma = st.selectbox("Traducir a:", ["English", "Spanish", "French", "German"])

if st.button("TRADUCIR AHORA ✨"):
    if texto_input:
        try:
            # Proceso de traducción
            if motor == "Google (Gratis)":
                res = Translator().translate(texto_input, dest=idioma[:2].lower()).text
            else:
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": f"Translate to {idioma}: {texto_input}"}]
                )
                res = response.choices[0].message.content
            
            st.success(res)
            
            # --- GUARDAR EN LA CAJA DE MEMORIA ---
            nueva_entrada = {"original": texto_input, "traducido": res, "idioma": idioma}
            st.session_state.historial.insert(0, nueva_entrada) # Insertar al principio
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- PESTAÑA DE HISTORIAL (NUEVA) ---
with tab4:
    st.header("📜 Últimas Traducciones")
    if not st.session_state.historial:
        st.write("Aún no hay traducciones en esta sesión.")
    else:
        for item in st.session_state.historial[:5]: # Mostrar las últimas 5
            with st.expander(f"{item['original'][:30]}... -> {item['idioma']}"):
                st.write(f"**Original:** {item['original']}")
                st.write(f"**Traducción:** {item['traducido']}")
                st.markdown("---")
