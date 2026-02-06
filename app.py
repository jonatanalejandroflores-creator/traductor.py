import streamlit as st
import numpy as np
from PIL import Image
from deep_translator import GoogleTranslator

# Configuración y Estética Original
st.set_page_config(page_title="Traductor Pro Multi-Modo", layout="wide")

# Sidebar con tu diseño original
st.sidebar.image("logo_beta.png", width=150) # Asegúrate de que el logo esté en la carpeta
st.sidebar.title("Configuración")
st.sidebar.markdown("---")
st.sidebar.info("Desarrollado por Jonatan Alejandro Flores")

# Título Principal
st.title("🌐 Traductor Pro Multi-Modo")

# --- SECCIÓN 1: TRADUCTOR (Tu diseño de siempre) ---
tabs = st.tabs(["⌨️ Texto", "🎤 Voz", "📸 Imagen"])

with tabs[0]:
    texto_origen = st.text_area("Escribe aquí:", height=150)
    idioma_dest = st.selectbox("Idioma destino:", ["en", "es", "fr", "it", "pt", "de"], index=1)
    if st.button("TRADUCIR AHORA ✨"):
        if texto_origen:
            res = GoogleTranslator(source='auto', target=idioma_dest).translate(texto_origen)
            st.success(f"**Traducción:** {res}")

# --- SECCIÓN 2: ÁLGEBRA (El nuevo agregado debajo) ---
st.markdown("---")
st.header("📐 Laboratorio de Álgebra (NumPy)")
st.write("Carga los vectores de tu cuaderno para calcular el Producto Punto y Vectorial.")

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
    
    punto = np.dot(vec_a, vec_b)
    vectorial = np.cross(vec_a, vec_b)
    
    st.subheader("Resultados:")
    st.write(f"🔹 **Producto Punto:** {punto}")
    st.write(f"🔹 **Producto Vectorial:** ({vectorial[0]}, {vectorial[1]}, {vectorial[2]})")
