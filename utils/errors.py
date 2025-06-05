"""
utils/errors.py

Sistema centralizado de manejo de errores para el proyecto.
Define excepciones personalizadas y funciones para capturar y registrar errores.
"""

from typing import Optional, Dict, Any
from utils.logger import log_error, log_critical
from config import DEBUG_MODE

# -----------------------------
# Clases de excepciones personalizadas
# -----------------------------
class ClassificationError(Exception):
    """
    Excepción base para errores relacionados con la clasificación de mensajes.
    """
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class ModelLoadingError(ClassificationError):
    """Error al cargar el modelo de Hugging Face."""
    pass

class InvalidInputError(ClassificationError):
    """Error por entrada inválida (texto vacío, formato incorrecto)."""
    pass

class APIError(ClassificationError):
    """Error al llamar a una API externa."""
    pass

class ConfigurationError(ClassificationError):
    """Error en la configuración del sistema."""
    pass

class UnexpectedError(ClassificationError):
    """Error inesperado o desconocido."""
    pass

# -----------------------------
# Función de manejo global de errores
# -----------------------------
def handle_error(exception: Exception) -> Dict[str, Any]:
    """
    Captura cualquier excepción, registra detalles y devuelve un mensaje estructurado.

    Args:
        exception: La excepción capturada.

    Returns:
        Dict[str, Any]: Respuesta estructurada con detalles del error.
    """
    if isinstance(exception, ClassificationError):
        error_type = exception.__class__.__name__
        log_critical(f"{error_type}: {str(exception)} | Detalles: {exception.details}", exc_info=True)
    else:
        error_type = "UnexpectedError"
        log_critical(f"{error_type}: {str(exception)}", exc_info=True)

    return {
        "error": error_type,
        "message": str(exception),
        "details": getattr(exception, "details", {}),
        "debug_mode": DEBUG_MODE
    }