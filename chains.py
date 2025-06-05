"""
chains.py

Cadenas personalizadas de LangChain para encapsular la lógica de clasificación.
Permite reutilizar la IA en FastAPI, Streamlit u otras interfaces.
"""

from langchain.chains.base import Chain
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

# Importar modelos y funciones necesarias
from models import MessageRequest, ClassificationResponse
from classifier import classify_message
from utils.logger import log_info, log_error
from utils.errors import handle_error

# -----------------------------
# Modelos de entrada y salida
# -----------------------------
class ClassificationInput(BaseModel):
    """Modelo para validar la entrada de la cadena."""
    message: str = Field(..., description="Mensaje de texto a clasificar")

class ClassificationOutput(BaseModel):
    """Modelo para devolver el resultado desde la cadena."""
    result: ClassificationResponse = Field(..., description="Resultado de la clasificación")

# -----------------------------
# Cadena personalizada de LangChain
# -----------------------------
class MessageClassificationChain(Chain):
    """
    Cadena personalizada que encapsula la lógica de clasificación.
    Permite usar la misma IA desde FastAPI, Streamlit o cualquier otra interfaz.
    """

    input_key: str = "message"  # Clave esperada en la entrada
    output_key: str = "result"  # Clave usada para devolver el resultado

    @property
    def input_keys(self) -> List[str]:
        """Claves de entrada requeridas por la cadena."""
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        """Claves de salida devueltas por la cadena."""
        return [self.output_key]

    def _call(self, inputs: Dict[str, Any], run_manager: Optional[Any] = None) -> Dict[str, Any]:
        """
        Ejecuta la lógica de clasificación encapsulada.

        Args:
            inputs (Dict[str, Any]): Diccionario con la entrada (ej: {"message": "Texto"})
            run_manager (Optional[Any]): Gestor de ejecución de LangChain (opcional)

        Returns:
            Dict[str, Any]: Diccionario con el resultado (ej: {"result": {...}})
        """
        message = inputs[self.input_key]
        log_info("Ejecutando MessageClassificationChain")

        try:
            # Validar entrada usando el modelo de Pydantic
            request = MessageRequest(message=message)
            
            # Ejecutar lógica de clasificación
            result = classify_message(request.message)
            
            # Devolver resultado como dict
            return {self.output_key: result}
        
        except Exception as e:
            # Manejar errores con el sistema centralizado
            error_response = handle_error(e)
            log_error(f"Error en cadena de clasificación: {error_response['message']}")
            return {self.output_key: error_response}

    @classmethod
    def from_config(cls, **kwargs) -> "MessageClassificationChain":
        """
        Crea una instancia de la cadena desde configuraciones globales.
        (Puede extenderse para cargar modelos, configuraciones adicionales, etc.)
        """
        return cls(**kwargs)

# -----------------------------
# Ejemplo de uso (para pruebas locales)
# -----------------------------
if __name__ == "__main__":
    # Crear instancia de la cadena
    chain = MessageClassificationChain()

    # Casos de prueba
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
            result = chain.run(text)
            if 'result' in result and isinstance(result['result'], dict):
                classification = result['result'].get('classification', 'Desconocido')
                confidence = result['result'].get('confidence', 0)
                print(f"Resultado: {classification} ({confidence:.2%})")
            else:
                print(f"Error: {result.get('result', {}).get('message', 'Error desconocido')}")
        except Exception as e:
            print(f"Error: {e}")