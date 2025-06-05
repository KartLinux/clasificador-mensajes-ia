"""
classifier.py

Lógica de clasificación de mensajes utilizando Zero-Shot Classification de Hugging Face.
Integra logging, manejo de errores personalizados y configuraciones globales.
"""

from transformers import pipeline
from config import MODEL_NAME, CANDIDATE_LABELS, CONFIDENCE_THRESHOLD
from utils.logger import log_info, log_debug, log_error, log_warning
from utils.errors import ModelLoadingError, InvalidInputError, UnexpectedError

# -----------------------------
# Carga global del modelo (una sola vez)
# -----------------------------
try:
    log_info(f"Cargando modelo de clasificación: {MODEL_NAME}")
    classifier = pipeline("zero-shot-classification", model=MODEL_NAME)
    log_debug(f"Modelo '{MODEL_NAME}' cargado correctamente")
except Exception as e:
    log_error(f"No se pudo cargar el modelo '{MODEL_NAME}': {str(e)}")
    raise ModelLoadingError(f"No se pudo cargar el modelo '{MODEL_NAME}'", details={"error": str(e)})

# -----------------------------
# Función principal de clasificación
# -----------------------------
def classify_message(text: str) -> dict:
    """
    Clasifica un mensaje en una de las categorías definidas usando Zero-Shot Classification.

    Args:
        text (str): Mensaje de texto a clasificar.

    Returns:
        dict: Resultado con la categoría y confianza (ej: {"classification": "Urgente", "confidence": 0.96}).

    Raises:
        InvalidInputError: Si el texto es inválido o vacío.
        UnexpectedError: Si ocurre un error inesperado durante la clasificación.
    """
    log_info("Iniciando clasificación de mensaje")

    # Validación básica del mensaje
    if not text or not text.strip():
        log_error("Mensaje vacío o inválido")
        raise InvalidInputError("El mensaje no puede estar vacío")

    log_debug(f"Texto a clasificar: '{text[:100]}...'")  # Mostrar solo los primeros 100 caracteres

    try:
        # Ejecutar Zero-Shot Classification
        result = classifier(text, candidate_labels=CANDIDATE_LABELS)

        # Obtener la categoría con mayor confianza
        classification = result["labels"][0]
        confidence = result["scores"][0]

        log_debug(f"Resultado crudo del modelo: {result}")
        log_info(f"Clasificación final: {classification} ({confidence:.2%})")

        # Verificar umbral de confianza
        if confidence < CONFIDENCE_THRESHOLD:
            log_warning(f"Confianza baja ({confidence:.2%}) para el mensaje: '{text[:100]}...'")

        return {
            "classification": classification,
            "confidence": confidence,
            "details": {
                "labels": result["labels"],
                "scores": result["scores"]
            }
        }

    except Exception as e:
        log_error(f"Error durante la clasificación: {str(e)}")
        raise UnexpectedError(f"Error durante la clasificación: {str(e)}", details={"error": str(e)}) from e

# -----------------------------
# Ejemplo de uso (para pruebas locales)
# -----------------------------
if __name__ == "__main__":
    test_cases = [
        "El edificio está en llamas.",
        "El informe se retrasará un día.",
        "Hay un problema menor en el sistema.",
        "",
        "Texto muy largo " * 100
    ]

    for i, text in enumerate(test_cases):
        print(f"\n--- Test {i+1}: '{text[:30]}'...")
        try:
            result = classify_message(text)
            print(f"Resultado: {result['classification']} ({result['confidence']:.2%})")
        except Exception as e:
            print(f"Error: {e}")