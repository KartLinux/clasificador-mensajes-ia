"""
config.py

Este archivo contiene todas las configuraciones globales del proyecto,
como etiquetas de clasificación, modelo de IA a usar, umbrales de confianza,
configuración de logs y otros parámetros reutilizables.

Evita repetir valores en múltiples archivos y centraliza la gestión de configuraciones.
"""

# -----------------------------
# Categorías de clasificación
# -----------------------------
# Etiquetas posibles para los mensajes
CANDIDATE_LABELS = ["Urgente", "Moderado", "Normal"]

# -----------------------------
# Configuración del modelo IA
# -----------------------------
# Nombre del modelo de Hugging Face para Zero-Shot Classification
MODEL_NAME = "facebook/bart-large-mnli"

# Longitud máxima de texto permitida para el modelo
MAX_LENGTH = 512  # BART maneja hasta 512 tokens

# Umbral mínimo de confianza para aceptar una clasificación
CONFIDENCE_THRESHOLD = 0.5  # 50% de confianza mínima

# -----------------------------
# Configuración de logs
# -----------------------------
# Nivel de logs: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "DEBUG"#"INFO"

# Formato predeterminado para mensajes de log
LOG_FORMAT = "<level>{level: <8}</level> | {time:YYYY-MM-DD HH:mm:ss} | {message}"

# -----------------------------
# Modo de depuración
# -----------------------------
# Activa funcionalidades extra para desarrollo
DEBUG_MODE = False  # Cambiar a True en entornos de prueba

# -----------------------------
# Configuraciones adicionales (ejemplo)
# -----------------------------
# Tiempo máximo de espera para llamadas externas (en segundos)
REQUEST_TIMEOUT = 10