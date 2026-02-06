import streamlit as st
import numpy as np
from PIL import Image
from deep_translator import GoogleTranslator

# Configuración de la página
st.set_page_config(page_title="Traductor Pro & Algebra Lab", layout="wide")

# Sidebar - Menú principal
st.sidebar.title("🚀 Menú de Herramientas")
pestana = st.sidebar.radio("Selecciona una función:", ["🌍 Traductor", "📐 Algebra Lab", "🖼️ Procesar Imagen"])

# --- PESTAÑA 1: TRADUCTOR ---
if pestana == "🌍 Traductor":
    st.title("🌍 Traductor Multi-Modo")
    texto_origen = st.text_area("Escribe aquí lo que quieras traducir:")
    idioma_dest = st.selectbox("Idioma destino:", ["es", "en", "fr", "it", "de", "pt"])
    
    if st.button("Traducir Ahora ✨"):
        if texto_origen:
            traduccion = GoogleTranslator(source='auto', target=idioma_dest).translate(texto_origen)
            st.success(f"**Resultado:** {traduccion}")
        else:
            st.warning("Por favor, ingresa un texto.")

# --- PESTAÑA 2: ALGEBRA LAB (Aquí usamos NumPy) ---
elif pestana == "📐 Algebra Lab":
    st.title("📐 Laboratorio de Álgebra de Vectores")
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

    vec_a = np.array([ax, ay, az])
    vec_b = np.array([bx, by, bz])

    if st.button("CALCULAR OPERACIONES 🧮"):
        # Cálculos con NumPy
        punto = np.dot(vec_a, vec_b)
        vectorial = np.cross(vec_a, vec_b)
        
        st.divider()
        st.subheader("Resultados:")
        st.write(f"🔹 **Producto Punto ($\vec{{a}} \cdot \vec{{b}}$):** {punto}")
        st.write(f"🔹 **Producto Vectorial ($\vec{{a}} \\times \vec{{b}}$):** ({vectorial[0]}, {vectorial[1]}, {vectorial[2]})")
        
        if punto == 0:
            st.success("✅ ¡Los vectores son **ortogonales** (forman 90°), como en tu ejercicio!")

# --- PESTAÑA 3: PROCESAR IMAGEN ---
elif pestana == "🖼️ Procesar Imagen":
    st.title("🖼️ Procesador de Imágenes")
    archivo = st.file_uploader("Sube una foto de tus apuntes:", type=["jpg", "png", "jpeg"])
    if archivo:
        img = Image.open(archivo)
        st.image(img, caption="Imagen cargada", use_column_width=True)
        st.info("Función de análisis de imagen activa.")

st.sidebar.info("Desarrollado por Jonatan Alejandro Flores")
