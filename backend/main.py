"""
backend/main.py

Servicio REST con FastAPI para clasificar mensajes de texto.
Usa la cadena de LangChain definida en `chains.py` y devuelve respuestas estructuradas con Pydantic.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from chains import MessageClassificationChain
from models import MessageRequest, ClassificationResponse, ErrorResponse
from utils.logger import log_info, log_error
from utils.errors import handle_error

# -----------------------------
# Inicialización de la aplicación
# -----------------------------
app = FastAPI(
    title="Clasificador de Mensajes",
    description="API REST para clasificar mensajes en categorías: Urgente, Moderado, Normal",
    version="1.0.0"
)

# -----------------------------
# Configuración de CORS (opcional pero recomendado)
# -----------------------------
origins = ["*"]  # Permite todas las orígenes (ajustar para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Instancia de la cadena de clasificación
# -----------------------------
classification_chain = MessageClassificationChain()

# -----------------------------
# Middleware de logs (opcional pero útil)
# -----------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar todas las solicitudes y respuestas.
    """
    log_info(f"Petición recibida: {request.method} {request.url}")
    response = await call_next(request)
    log_info(f"Respuesta enviada: {response.status_code}")
    return response

# -----------------------------
# Endpoint de clasificación
# -----------------------------
@app.post("/classify", response_model=ClassificationResponse, responses={400: {"model": ErrorResponse}})
async def classify_message_endpoint(request: MessageRequest):
    """
    Endpoint para clasificar un mensaje de texto.
    
    Args:
        request (MessageRequest): Mensaje de texto a clasificar.
    
    Returns:
        ClassificationResponse: Resultado de la clasificación.
    """
    try:
        result = classification_chain.invoke({"message": request.message})
        # Devuelve el resultado directamente
        return result["result"]
    
    except Exception as e:
        error_response = handle_error(e)
        return ClassificationResponse(
            classification="Error",
            confidence=0.0,
            details=error_response
        )

# -----------------------------
# Punto de entrada para ejecutar el servidor
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)