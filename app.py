import os
import streamlit as st
import openai
from googletrans import Translator
import numpy as np

# --- CONFIGURACIÓN DE SEGURIDAD Y PÁGINA ---
api_key_env = os.getenv("OPENAI_API_KEY")
st.set_page_config(page_title="AI Trans Pro + Algebra Lab", page_icon="🌐", layout="wide")

# --- INICIALIZAR MEMORIA ---
if "historial" not in st.session_state:
    st.session_state.historial = []

# --- BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.title("⚙️ Configuración")
    if api_key_env and api_key_env.startswith("sk-"):
        st.success("✅ API Key en Secrets")
        api_key = api_key_env
    else:
        api_key = st.text_input("Ingresar OpenAI API Key:", type="password")
    
    openai.api_key = api_key
    motor = st.selectbox("Motor de Traducción:", ["Google (Gratis)", "ChatGPT (Premium)"])

# --- CUERPO PRINCIPAL ---
st.title("🌐 AI Trans Pro & 🧮 Algebra Lab")

# Definición de Pestañas (Sumamos la de Álgebra)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen", "📜 Historial", "📐 Algebra Lab"])

# --- TRADUCCIÓN DE TEXTO ---
with tab1:
    texto_input = st.text_area("Escribe para traducir:", key="txt_input")
    idioma = st.selectbox("Traducir a:", ["English", "Spanish", "French", "German"], key="lang_txt")
    
    if st.button("TRADUCIR TEXTO ✨"):
        if texto_input:
            try:
                if motor == "Google (Gratis)":
                    res = Translator().translate(texto_input, dest=idioma[:2].lower()).text
                else:
                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": f"Translate to {idioma}: {texto_input}"}]
                    )
                    res = response.choices[0].message.content
                
                st.success(f"**Resultado:** {res}")
                st.session_state.historial.insert(0, {"original": texto_input, "traducido": res, "idioma": idioma})
            except Exception as e:
                st.error(f"Error: {e}")

# --- LABORATORIO DE ÁLGEBRA (Lo nuevo para tu facultad) ---
with tab5:
    st.header("🧮 Calculadora de Álgebra Lineal y Complejos")
    opcion_algebra = st.radio("Selecciona el tema:", ["Vectores R3", "Números Complejos", "Lógica Booleana"])

    if opcion_algebra == "Vectores R3":
        st.subheader("Operaciones con Vectores (Como en tu cuaderno)")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Vector A**")
            ax = st.number_input("x", value=3, key="ax")
            ay = st.number_input("y", value=-2, key="ay")
            az = st.number_input("z", value=1, key="az")
        with col2:
            st.write("**Vector B**")
            bx = st.number_input("x ", value=0, key="bx")
            by = st.number_input("y ", value=4, key="by")
            bz = st.number_input("z ", value=-3, key="bz")
        
        vec_a = np.array([ax, ay, az])
        vec_b = np.array([bx, by, bz])
        
        if st.button("Calcular Vectores 📐"):
            prod_punto = np.dot(vec_a, vec_b)
            prod_vectorial = np.cross(vec_a, vec_b)
            mag_a = np.linalg.norm(vec_a)
            
            st.write(f"**Producto Punto ($\vec{{a}} \cdot \vec{{b}}$):** {prod_punto}")
            st.write(f"**Producto Vectorial ($\vec{{a}} \\times \vec{{b}}$):** {prod_vectorial}")
            st.write(f"**Magnitud de A:** {mag_a:.2f}")
            
            if prod_punto == 0:
                st.success("✅ Los vectores son ORTOGONALES (90°)")
            else:
                st.warning("❌ No son ortogonales")

    elif opcion_algebra == "Números Complejos":
        st.subheader("Multiplicación de Complejos")
        st.write("Ejemplo de tu hoja: $(3 - 1i) * (2 + 5i)$")
        c1_re = st.number_input("Z1 Real", value=3)
        c1_im = st.number_input("Z1 Imag", value=-1)
        c2_re = st.number_input("Z2 Real", value=2)
        c2_im = st.number_input("Z2 Imag", value=5)
        
        z1 = complex(c1_re, c1_im)
        z2 = complex(c2_re, c2_im)
        
        if st.button("Multiplicar Z1 * Z2"):
            res_z = z1 * z2
            st.success(f"**Resultado:** {res_z} (En Python 'j' es 'i')")

# --- PESTAÑA DE HISTORIAL ---
with tab4:
    st.header("📜 Historial de Sesión")
    for item in st.session_state.historial:
        st.text(f"{item['original']} -> {item['traducido']} ({item['idioma']})")
