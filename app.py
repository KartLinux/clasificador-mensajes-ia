"""
frontend/app.py

Interfaz gráfica con Streamlit para enviar mensajes y ver resultados de clasificación.
Usa el servicio REST de FastAPI y muestra resultados con formato visual.
"""

import streamlit as st
import requests
from config import CANDIDATE_LABELS, CONFIDENCE_THRESHOLD
from models import MessageRequest, ClassificationResponse
from utils.logger import log_info, log_debug, log_error
from utils.errors import handle_error

# -----------------------------
# Configuración inicial de la aplicación
# -----------------------------
st.set_page_config(
    page_title="Clasificador de Mensajes",
    page_icon="🚨",
    layout="centered"
)

st.title("🚨 Clasificador de Mensajes")
st.markdown("Ingresa un mensaje y obtén su clasificación en tiempo real.")

# -----------------------------
# Estado de sesión para historial
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Función para enviar mensaje al backend
# -----------------------------
def classify_message(text):
    """
    Envía un mensaje al backend y devuelve el resultado de clasificación.

    Args:
        text (str): Mensaje de texto a clasificar.

    Returns:
        dict: Resultado con clasificación y confianza.
    """
    log_info("Enviando mensaje al backend")
    try:
        response = requests.post("http://localhost:8000/classify", json={"message": text})
        log_debug(f"Respuesta del backend: {response.json()}")
        
        if response.status_code == 200:
            return response.json()
        else:
            error_response = response.json()
            raise Exception(error_response.get("message", "Error desconocido"))
    
    except Exception as e:
        log_error(f"Error al comunicarse con el backend: {str(e)}")
        return handle_error(e)

# -----------------------------
# Interfaz de usuario
# -----------------------------
with st.form(key="classification_form"):
    message_input = st.text_area("Escribe tu mensaje aquí:", height=200, placeholder="Ej: Hay un incendio en la oficina")
    submit_button = st.form_submit_button(label="Clasificar")

# -----------------------------
# Procesamiento y visualización de resultados
# -----------------------------
# En app.py
if submit_button:
    result = classify_message(message_input)

    if "error" in result:
        st.error(f"🚨 Error: {result['message']}")
    else:
        classification = result["classification"]
        confidence = result["confidence"]

        # Mostrar resultado con estilo condicional
        if classification == "Urgente":
            color = "red"
        elif classification == "Moderado":
            color = "orange"
        else:
            color = "green"

        # Ajustar opacidad si la confianza es baja
        opacity = "FF" if confidence > CONFIDENCE_THRESHOLD else "66"  # FF = 100%, 66 = 40%

        st.markdown(f"""
        <div style="padding: 15px; border-radius: 8px; background-color: {color}{opacity}; color: {color}; font-weight: bold;">
            ⚠️ Categoría: {classification} | Confianza: {confidence * 100:.1f}%
        </div>
        """, unsafe_allow_html=True)

        # Mostrar advertencia si confianza es baja
        if confidence < CONFIDENCE_THRESHOLD:
            st.warning(f"⚠️ La confianza es baja ({confidence * 100:.1f}%), la clasificación puede no ser precisa.")

# -----------------------------
# Historial de mensajes clasificados
# -----------------------------
if st.session_state.history:
    st.markdown("---")
    st.subheader("📜 Historial de Clasificaciones")
    for item in st.session_state.history:
        st.text(f"{item['timestamp']} | {item['classification']} ({item['confidence']:.1%}): {item['message'][:50]}...")

# -----------------------------
# Barra lateral con información
# -----------------------------
st.sidebar.title("🔧 Configuración")
st.sidebar.markdown(f"**Etiquetas disponibles:** {', '.join(CANDIDATE_LABELS)}")
st.sidebar.markdown(f"**Umbral de confianza:** {CONFIDENCE_THRESHOLD:.0%}")
st.sidebar.markdown("**Backend:** FastAPI")
st.sidebar.markdown("**Modelo:** facebook/bart-large-mnli")