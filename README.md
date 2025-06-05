clasificador-mensajes/
│
├── backend/
│   ├── main.py           # Punto de entrada de FastAPI
│
├── frontend/
│   └── app.py            # Interfaz gráfica con Streamlit
│
├── utils/
│   ├── logger.py         # Configuración de eventos (INFO, DEBUG, ERROR).
│   └── errors.py         # Manejo centralizado de errores
│
├── config.py             # Constantes globales (modelos, etiquetas, modelo, umbral de confianza.)
├── chains.py             # Cadenas personalizadas de LangChain para reutilización
├── models.py             # Modelos Pydantic para validación de datos
├── classifier.py         # Clasificador con Zero-Shot + LangChain
├── requirements.txt      # Dependencias del entorno
└── README.md             # Documentación del proyecto

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