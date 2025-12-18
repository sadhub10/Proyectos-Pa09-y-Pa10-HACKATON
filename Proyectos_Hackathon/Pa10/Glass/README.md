# Healthy Station 🏥
### Sistema Inteligente de Apoyo al Diagnóstico Médico

**Healthy Station** es una plataforma integral desarrollada por el grupo **Glass (Giving Logical Software Solutions)**. Este proyecto se presenta como un MVP (Producto Mínimo Viable) de visión artificial diseñado para asistir a profesionales de la salud en la detección temprana de patologías mediante el análisis automatizado de imágenes médicas.

---

## 🚀 Características del Proyecto

* **Gestión de Expedientes:** Permite la creación y consulta de nuevos expedientes clínicos para pacientes, manteniendo un historial organizado de cada consulta.
* **Análisis Multiclase (Neumonía):** Procesamiento de radiografías de tórax para clasificar entre: *Saludable, Neumonía Bacteriana o Neumonía Viral*.
* **Análisis Binario (Tumor Cerebral):** Procesamiento de resonancias magnéticas (MRI) para detectar la presencia o ausencia de masas tumorales.
* **Persistencia de Datos:** Integración con **SQLite** mediante **SQLModel** para registrar cada chequeo, asociándolo automáticamente al expediente del paciente.
* **Interfaz Médica:** Frontend moderno y amigable construido en **Streamlit**.

---

## 🧠 Módulos de Inteligencia Artificial

El núcleo del sistema se basa en Redes Neuronales Convolucionales (CNN) en formato `.keras`, optimizados mediante técnicas de *Transfer Learning* y *Fine-Tuning*:

1.  **Modelo de Neumonía (`modelo_neumonia.keras`):**
    * **Arquitectura:** Basada en VGG16.
    * **Salida:** Multiclase (3 neuronas con activación Softmax).
    * **Entrada:** Radiografías de tórax reescaladas a 224x224 px.

2.  **Modelo de Tumor Cerebral (`modelo_tumor.keras`):**
    * **Arquitectura:** EfficientNetB0.
    * **Salida:** Binaria (1 neurona con activación Sigmoidea).
    * **Entrada:** Resonancias magnéticas reescaladas a 224x224 px.

---

## 🛠️ Stack Tecnológico

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend / API:** [FastAPI](https://fastapi.tiangolo.com/) (con gestión de ciclo de vida `lifespan`)
* **Modelos de IA:** TensorFlow / Keras
* **Base de Datos / ORM:** SQLite / SQLModel
* **Servidor ASGI:** Uvicorn

---


## 📦 Dependencias Core

Para replicar el entorno de ejecución, se requieren las siguientes librerías:

```text
streamlit
fastapi
sqlmodel
uvicorn
tensorflow
python-multipart
pillow
numpy
```

## 📂 Persistencia de Datos (SQLite)

El sistema utiliza una base de datos **SQLite** local para garantizar la portabilidad y rapidez. La estructura incluye:

* **Tabla `Pacientes`:** Almacena datos demográficos e identificadores únicos.
* **Tabla `Chequeos`:** Registra cada análisis realizado, incluyendo la fecha, el tipo de modelo usado, la predicción de la IA y el nivel de confianza (probabilidad).

---

## 💻 Configuración del Entorno

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

**Clonar el repositorio:**
```bash
git clone [https://github.com/tu-usuario/healthy-station.git](https://github.com/tu-usuario/healthy-station.git)
cd healthy-station
streamlit run app.py
```
## ⚠️ Descargo de Responsabilidad (Disclaimer)

Este sistema es un prototipo de investigación y una herramienta de apoyo al diagnóstico. No sustituye bajo ninguna circunstancia el criterio, diagnóstico o tratamiento de un médico profesional. Los resultados generados por los modelos de IA deben ser interpretados únicamente como una sugerencia técnica.

## 👤 Autores

Este proyecto fue desarrollado por el equipo de Glass (Giving Logical Software Solutions):

    Steven Ampie - Desarrollo de Modelo de Pneumonia

    Arland Barrera - Desarrollo de Modelo de Tumor Cerebral

    Anel Ruiz - Desarrollo Frontend / Streamlit

    Haneff Botello - Arquitectura de Base de Datos

2025 - Healthy Station Project

