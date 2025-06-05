"""
models.py

Modelos de datos para validación de entrada/salida en la API REST.
Usa Pydantic para garantizar que los mensajes sean válidos y las respuestas tengan formato correcto.
"""

from pydantic import BaseModel, model_validator
from typing import Optional
from config import MAX_LENGTH
from utils.errors import InvalidInputError
from utils.logger import log_error

# -----------------------------
# Modelo de solicitud de entrada
# -----------------------------
class MessageRequest(BaseModel):
    message: str

    @model_validator(mode="after")
    def validate_message(self):
        value = self.message
        if not value.strip():
            raise InvalidInputError("El mensaje no puede estar vacío")
        
        if len(value) > MAX_LENGTH:
            log_error(f"Texto demasiado largo ({len(value)} caracteres). Truncado a {MAX_LENGTH}.")
            self.message = value[:MAX_LENGTH]
        
        return self

# -----------------------------
# Modelo de respuesta de clasificación
# -----------------------------
class ClassificationResponse(BaseModel):
    classification: str
    confidence: float
    details: Optional[dict] = {}

    @model_validator(mode="after")
    def validate_confidence(self):
        value = self.confidence
        if not 0 <= value <= 1:
            raise ValueError("La confianza debe estar entre 0 y 1")
        return self

# -----------------------------
# Modelo para respuestas de error
# -----------------------------
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = {}