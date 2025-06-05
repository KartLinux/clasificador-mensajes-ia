"""
utils/logger.py

Sistema centralizado de logs para registrar eventos, errores y operaciones del sistema.
Usa la librería `loguru` para simplificar el registro de mensajes con niveles de detalle:
- DEBUG: Detalles técnicos para depuración.
- INFO: Mensajes informativos sobre operaciones normales.
- WARNING: Advertencias no críticas.
- ERROR: Errores que afectan la ejecución.
"""

from loguru import logger
import sys
from config import LOG_LEVEL, LOG_FORMAT, DEBUG_MODE

# -----------------------------
# Configuración inicial del logger
# -----------------------------
def setup_logger():
    """
    Configura el sistema de logs con limpieza de archivos anteriores
    y formato personalizado.
    """
    import os

    # Elimina logs antiguos
    log_dir = "logs"
    #if os.path.exists(log_dir):
        #for file in os.listdir(log_dir):
           # os.remove(os.path.join(log_dir, file))
    #else:
       # os.makedirs(log_dir)

    # Elimina configuraciones previas
    logger.remove()

    # Añade salida a consola
    logger.add(
        sys.stdout,
        level=LOG_LEVEL,
        format=LOG_FORMAT
    )

    # Guardado en archivo (opcional)
    logger.add(
        os.path.join(log_dir, "app.log"),
        level="INFO",
        format=LOG_FORMAT,
        rotation="10 MB",
        retention=1
    )

    return logger

# -----------------------------
# Instancia global del logger
# -----------------------------
# Configura y expone el logger para ser usado en otros archivos
setup_logger()

# -----------------------------
# Funciones de registro simplificadas
# -----------------------------
def log_info(message: str):
    """Registra un mensaje informativo."""
    logger.info(message)

def log_debug(message: str):
    """Registra detalles técnicos para depuración."""
    logger.debug(message)

def log_warning(message: str):
    """Registra una advertencia no crítica."""
    logger.warning(message)

def log_error(message: str):
    """Registra un error crítico."""
    logger.error(message)

def log_critical(message: str):
    """Registra un error fatal que detiene la ejecución."""
    logger.critical(message)

def log_critical(message: str, exc_info: bool = False):
    logger.critical(message, exc_info=exc_info)

def log_error(message: str, exc_info: bool = False):
    logger.error(message, exc_info=exc_info)