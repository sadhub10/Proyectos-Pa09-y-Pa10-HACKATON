# Healthy Station 🏥
### Sistema Inteligente de Apoyo al Diagnóstico Médico

**Healthy Station** es una plataforma integral desarrollada por el grupo **Glass (Giving Logical Software Solutions)**. Este proyecto se presenta como un MVP (Producto Mínimo Viable) de visión artificial diseñado para asistir a profesionales de la salud en la detección temprana de patologías mediante el análisis automatizado de imágenes médicas.

---

## 🚀 Características del Proyecto

* **Detección de Patologías:** Implementación de modelos de aprendizaje profundo para identificar anomalías en tiempo real.
* **Gestión de Expedientes:** Sistema de registro de pacientes y almacenamiento de historial de consultas.
* **Segunda Opinión Médica:** Herramienta orientada a reducir la carga de análisis inicial y ayudar a priorizar casos críticos.
* **Interfaz Web:** Panel de control interactivo construido para ser ligero y accesible desde cualquier navegador.

---

## 🧠 Módulos de Inteligencia Artificial

El núcleo del sistema se basa en Redes Neuronales Convolucionales (CNN) entrenadas específicamente para dos áreas críticas:

### 1. Clasificación de Tumores Cerebrales (MRI)
* **Modelo:** `EfficientNetB0`
* **Entrada:** Resonancias Magnéticas (MRI).
* **Clases:** `Healthy` (Sano) / `Tumor` (Tumor detectado).
* **Tecnología:** Utiliza *Transfer Learning* para aprovechar la eficiencia de parámetros de la arquitectura EfficientNet, optimizando la precisión en dispositivos con recursos limitados.

### 2. Detección de Pneumonía (Rayos X)
* **Modelo:** `VGG16`
* **Entrada:** Radiografías de Tórax.
* **Clases:** `Normal` / `Pneumonia`.
* **Tecnología:** Emplea la arquitectura clásica VGG16, conocida por su excelente capacidad de extracción de características en texturas médicas y opacidades pulmonares.

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Frontend / Interfaz** | [Streamlit](https://streamlit.io/) |
| **Lenguaje de Programación** | Python 3.x |
| **Deep Learning** | TensorFlow / Keras |
| **Base de Datos** | SQLite3 |
| **Procesamiento de Imágenes** | OpenCV / PIL |

---

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
⚠️ Descargo de Responsabilidad (Disclaimer)

Este sistema es un prototipo de investigación y una herramienta de apoyo al diagnóstico. No sustituye bajo ninguna circunstancia el criterio, diagnóstico o tratamiento de un médico profesional. Los resultados generados por los modelos de IA deben ser interpretados únicamente como una sugerencia técnica.

👤 Autores

Este proyecto fue desarrollado por el equipo de Glass (Giving Logical Software Solutions):

    Steven Ampie - Desarrollo de Modelo de Pneumonia

    Arland Barrera - Desarrollo de Modelo de Tumor Cerebral

    Anel Ruiz - Desarrollo Frontend / Streamlit

    Haneff Botello - Arquitectura de Base de Datos

2025 - Healthy Station Project
