
# 🦾 CoreScripts – Sistema de Asistencia Visual Inteligente

## 👥 Nombre del equipo

**Equipo CoreScripts**

## 📌 Integrantes del equipo

* **Gabriel Valderrama** – Visión Artificial y Captura / Interpretación Semántica
* **Gustavo De la Rivera** – Visión Artificial y Captura / Interpretación Semántica
* **Joel Monrroy** – Lenguaje Natural, Texto a Voz, Integración y Documentación
* **Manuel Rojas** – Lenguaje Natural, Texto a Voz, Integración y Documentación

---

## 🎯 Nombre del proyecto

**VISUAL-VOICE – Sistema de Asistencia Visual Inteligente**

---

## 🧠 Planteamiento del problema

Las personas con discapacidad visual enfrentan limitaciones significativas para desplazarse de forma autónoma en entornos cotidianos, debido a la imposibilidad de identificar obstáculos, personas u objetos cercanos. A pesar de los avances tecnológicos, muchas soluciones existentes son costosas o poco accesibles. Surge así la necesidad de desarrollar un sistema inteligente que combine visión artificial y retroalimentación auditiva para mejorar la orientación y seguridad del usuario.

---

🧪 Entorno de desarrollo

Todo el proyecto VISUAL-VOICE se ejecuta dentro de un entorno virtual de Python, con el objetivo de aislar dependencias, garantizar compatibilidad entre librerías y facilitar la replicación del sistema en otros equipos.

El uso de un entorno virtual permite:

Evitar conflictos entre versiones de librerías

Mantener el proyecto organizado

Facilitar la instalación y ejecución del sistema

---

▶️ Instrucciones de ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/usuario/visual-voice.git
cd visual-voice
2️⃣ Crear el entorno virtual
python -m venv venv
3️⃣ Activar el entorno virtual

En Windows:

venv\Scripts\activate

En Linux / macOS:

source venv/bin/activate
4️⃣ Instalar dependencias
pip install -r requirements.txt
5️⃣ Ejecutar el sistema
python main.py

Al ejecutarse, el asistente activará la cámara, detectará objetos en tiempo real y generará descripciones auditivas del entorno

## 🎯 Objetivo general

Desarrollar un asistente visual inteligente capaz de detectar objetos en tiempo real mediante visión artificial y comunicar dicha información al usuario a través de descripciones auditivas claras.

### Objetivos específicos

* Implementar detección de objetos en tiempo real usando modelos de visión artificial.
* Interpretar semánticamente la posición y distancia de los objetos detectados.
* Generar descripciones en lenguaje natural comprensibles para el usuario.
* Convertir dichas descripciones en audio mediante técnicas de Text-to-Speech.
* Integrar todos los módulos en un sistema funcional.

---

## 🧩 Aplicación general del proyecto

SAVI está diseñado como una herramienta de apoyo para personas con discapacidad visual, permitiéndoles reconocer su entorno inmediato a través de indicaciones auditivas. El sistema puede ser utilizado en interiores o exteriores, ayudando a identificar personas, obstáculos y elementos relevantes para una navegación más segura.

---

## 🛠️ Herramientas y tecnologías utilizadas

* **Lenguaje de programación:** Python
* **Visión artificial:** OpenCV
* **Modelo de detección:** YOLO (v5 / v8)
* **Procesamiento semántico:** Reglas lógicas personalizadas
* **Lenguaje natural:** Plantillas de generación de texto
* **Text-to-Speech:** pyttsx3 / gTTS
* **Control de versiones:** Git y GitHub

---

## 📂 Distribución del trabajo y funciones

### 🔹 Integrante 1 – Visión Artificial y Captura

**Rol:** Responsable del módulo de percepción visual

**Funciones:**

* Configuración del entorno de desarrollo (Python y librerías)
* Captura de video en tiempo real con OpenCV
* Integración del modelo YOLO
* Ajuste de clases de interés (persona, silla, puerta, etc.)
* Visualización de bounding boxes
* Medición de latencia de detección

**Entregables:**

* Código funcional de detección
* Video demostrativo
* Explicación técnica

---

### 🔹 Integrante 2 – Interpretación Semántica y Lógica

**Rol:** Responsable del razonamiento y reglas inteligentes

**Funciones:**

* Análisis de la salida del modelo YOLO
* Definición de reglas de posición (izquierda, frente, derecha)
* Estimación de distancia según el tamaño del bounding box
* Priorización de objetos relevantes
* Generación de estructura de datos semántica

**Ejemplo de salida:**

```json
{
  "objeto": "persona",
  "posicion": "frente",
  "distancia": "cerca"
}
```

**Entregables:**

* Módulo semántico
* Documento de reglas
* Ejemplos de entrada y salida

---

### 🔹 Integrante 3 – Lenguaje Natural y Texto a Voz

**Rol:** Responsable de la comunicación con el usuario

**Funciones:**

* Diseño de plantillas de generación de texto
* Unión coherente de múltiples objetos
* Implementación de Text-to-Speech
* Ajuste de velocidad y claridad del audio
* Pruebas en escenarios reales

**Ejemplo de salida:**

> “Hay una persona frente a ti. A la derecha hay una silla.”

**Entregables:**

* Generador de texto
* Módulo TTS integrado
* Audio de prueba

---

### 🔹 Integrante 4 – Integración, Evaluación y Documentación

**Rol:** Coordinador técnico y académico

**Funciones:**

* Integración de todos los módulos
* Pruebas generales del sistema
* Definición de métricas de evaluación
* Redacción del informe final
* Creación del video demostrativo
* Preparación de la presentación

**Entregables:**

* Sistema completo funcional
* Informe final
* Video demostrativo
* Conclusiones y trabajo futuro

---

## ✅ Resultado del proyecto

Como resultado, se obtuvo un sistema funcional capaz de detectar objetos en tiempo real, interpretar su ubicación y comunicar esta información al usuario mediante descripciones auditivas claras. SAVI demuestra el potencial de la inteligencia artificial aplicada a la accesibilidad, ofreciendo una solución viable y escalable para mejorar la autonomía de personas con discapacidad visual.

---

## 📌 Trabajo futuro

* Integración con dispositivos móviles
* Mejora en la estimación de distancias
* Inclusión de reconocimiento de texto y señales
* Optimización del rendimiento en tiempo real

---

📍 *Proyecto desarrollado con fines académicos.*
