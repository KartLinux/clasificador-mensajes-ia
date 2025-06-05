## 📁 Estructura del Proyecto

| Carpeta / Archivo | Propósito |
|------------------|-----------|
| `backend/main.py` | Servidor REST con FastAPI |
| `frontend/app.py` | Interfaz web interactiva con Streamlit |
| `utils/logger.py` | Sistema de logs profesionales |
| `utils/errors.py` | Errores personalizados y manejo coherente |
| `config.py` | Configuraciones globales: etiquetas, modelo y umbral |
| `chains.py` | Cadena personalizada de LangChain |
| `models.py` | Validación de datos con Pydantic |
| `classifier.py` | Clasificación IA con Zero-Shot Classification |
| `requirements.txt` | Lista de dependencias del entorno |
| `README.md` | Documentación principal del proyecto |

# Clasificación Automatizada de Mensajes con IA

## 📌 Descripción
Sistema inteligente para clasificar mensajes de texto en tres categorías: **Urgente**, **Moderado** y **Normal**, usando **clasificación Zero-Shot** de Hugging Face integrada con **LangChain**, expuesta como API REST con **FastAPI** y visualizada mediante una interfaz interactiva con **Streamlit**.

Este proyecto fue desarrollado siguiendo buenas prácticas de arquitectura modular, separación de responsabilidades y reutilización de código, permitiendo fácil escalabilidad y mantenimiento.

---

## 🛠️ Tecnologías Usadas

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI + Uvicorn |
| IA | Hugging Face Transformers (Zero-Shot Classification) |
| Integración de IA | LangChain |
| Frontend | Streamlit |
| Logging | Loguru |
| Validación de Datos | Pydantic |
| Gestión de Errores | Custom Handlers |
| Configuración Global | Archivo `config.py` |

---

## 🧪 Requisitos del Sistema

- Python 3.9 o superior
- Sistema operativo: Windows, Linux o macOS
- Entorno virtual (recomendado: `venv`)
- Conexión a internet (para descargar modelos de Hugging Face)

---

## 📦 Instalación

1. **Crear entorno virtual (Windows):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
2. **Ejecuta el comando para instalar dependencias:**
   ```bash
   pip install -r requirements.txt
3. **Ejecuta el servidor FastAPI:**
   ```bash
   python -m uvicorn backend.main:app --reload
4. **Ejecuta la aplicación de Streamlit:**
   ```bash
   streamlit run frontend/app.py
