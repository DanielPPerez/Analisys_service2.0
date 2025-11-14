# test_interface.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io # <-- Importar la librería io

# Importamos el orquestador principal
from src.ml_core.analysis_service import AnalysisService

# --- CONFIGURACIÓN DE LA PÁGINA Y DEL SERVICIO ---

@st.cache_resource
def load_analysis_service():
    """Carga una instancia del AnalysisService."""
    print("Inicializando AnalysisService...")
    model_path = "ml_models/best_model.keras" 
    service = AnalysisService(model_path=model_path, use_llm_feedback=False)
    return service

# --- CONSTRUCCIÓN DE LA INTERFAZ DE USUARIO ---

st.set_page_config(page_title="Tutor de Caligrafía AI", layout="wide")
st.title("✍️ Interfaz de Prueba - Tutor de Caligrafía AI")
st.write(
    "Carga una imagen de una letra que hayas escrito y selecciona el caracter correspondiente "
    "para recibir un análisis detallado y consejos para mejorar."
)

analysis_service = load_analysis_service()

col1, col2 = st.columns(2)

with col1:
    st.header("1. Carga tu Imagen")
    uploaded_file = st.file_uploader(
        "Elige un archivo de imagen (PNG, JPG)",
        type=['png', 'jpg', 'jpeg']
    )

    st.header("2. Indica la Letra")
    character_input = st.text_input(
        "¿Qué letra intentabas escribir?",
        placeholder="Ej: A, b, g, Ch, ñ..."
    ).strip()

    analyze_button = st.button("Analizar Mi Letra", type="primary", use_container_width=True)

with col2:
    st.header("Tu Imagen")
    if uploaded_file is not None:
        # --- CAMBIO IMPORTANTE AQUÍ (Parte 1) ---
        # Leemos el contenido del archivo UNA SOLA VEZ y lo guardamos en una variable.
        # .getvalue() es seguro porque se puede llamar múltiples veces.
        image_bytes = uploaded_file.getvalue()
        
        # Usamos Pillow para mostrar la imagen desde los bytes en memoria.
        try:
            image_for_display = Image.open(io.BytesIO(image_bytes))
            st.image(image_for_display, caption="Imagen cargada", use_column_width=True)
        except Exception as e:
            st.error(f"No se pudo mostrar la imagen. ¿Es un formato válido? Error: {e}")
    else:
        st.info("El área de la imagen aparecerá aquí una vez que la cargues.")

# --- LÓGICA DE ANÁLISIS Y VISUALIZACIÓN ---

st.divider()

if analyze_button:
    # Usamos 'uploaded_file' para verificar que se subió algo, pero 'image_bytes' para procesar
    if 'image_bytes' not in locals():
        st.error("Por favor, carga una imagen primero.")
    elif not character_input:
        st.error("Por favor, indica qué letra intentabas escribir.")
    else:
        st.header("Resultados del Análisis")
        with st.spinner('Analizando tu trazo con IA...'):
            
            # --- CAMBIO IMPORTANTE AQUÍ (Parte 2) ---
            # Ya no leemos el archivo de nuevo. Usamos los 'image_bytes' que ya teníamos.
            np_array = np.frombuffer(image_bytes, np.uint8)
            opencv_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # --- CORRECCIÓN CRÍTICA: AÑADIMOS UNA VERIFICACIÓN ---
            if opencv_image is None:
                st.error("OpenCV no pudo decodificar la imagen. Por favor, asegúrate de que es un archivo de imagen válido (PNG, JPG) y no está corrupto.")
            else:
                # Si la imagen es válida, procedemos con el análisis
                results = analysis_service.analyze(
                    user_image_raw=opencv_image,
                    character_analyzed=character_input
                )

                if "error" in results:
                    st.error(f"Ocurrió un error en el análisis: {results['error']}")
                else:
                    feedback = results.get("feedback", {})
                    detailed_metrics = results.get("detailed_metrics", {})
                    
                    st.subheader("Feedback del Tutor")
                    st.success(f"✔️ **Fortalezas:** {feedback.get('fortalezas', 'N/A')}")
                    st.warning(f"🎯 **Áreas de Mejora:** {feedback.get('areas_mejora', 'N/A')}")
                    
                    with st.expander("Ver análisis técnico detallado (JSON)"):
                        st.json(detailed_metrics)