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

Las personas con discapacidad visual enfrentan limitaciones significativas para desplazarse de forma autónoma en entornos cotidianos, debido a la imposibilidad de identificar obstáculos, personas u objetos cercanos. A pesar de los avances tecnológicos, muchas soluciones existentes son costosas, dependen de conexión a internet o requieren hardware especializado. Surge así la necesidad de desarrollar un sistema inteligente, accesible y de bajo costo que combine visión artificial con retroalimentación auditiva en tiempo real para mejorar la orientación, seguridad y autonomía del usuario.

---

## 🧩 Descripción general del proyecto

VISUAL-VOICE es un prototipo de asistente visual que utiliza una cámara convencional y modelos de detección de objetos para interpretar el entorno inmediato del usuario. El sistema procesa el video en tiempo real, identifica objetos relevantes, infiere su posición y distancia aproximada, y genera descripciones auditivas claras mediante técnicas de Text-to-Speech (TTS). Todo el procesamiento se realiza localmente, priorizando la privacidad y el funcionamiento sin conexión.

---

## 🏗️ Arquitectura del sistema

El sistema está organizado en módulos independientes pero integrados:

1. **Captura y percepción visual**: adquisición de video y detección de objetos.
2. **Interpretación semántica**: análisis de resultados, reglas de prioridad, posición y distancia.
3. **Generación de lenguaje natural**: construcción de mensajes comprensibles para el usuario.
4. **Salida auditiva (TTS)**: conversión de texto a voz y reproducción.
5. **Orquestación e integración**: coordinación de módulos y control de flujo.

---

## 🔄 Flujo de funcionamiento

1. Activación de la cámara.
2. Captura de frames en tiempo real.
3. Detección de objetos mediante YOLO.
4. Filtrado y priorización de objetos relevantes.
5. Inferencia de posición (izquierda, frente, derecha) y distancia (cerca, media, lejos).
6. Generación de descripciones en lenguaje natural.
7. Conversión de texto a audio y reproducción al usuario.

---

## 🧪 Entorno de desarrollo

Todo el proyecto VISUAL-VOICE se ejecuta dentro de un entorno virtual de Python, con el objetivo de aislar dependencias, garantizar compatibilidad entre librerías y facilitar la replicación del sistema en otros equipos.

El uso de un entorno virtual permite:

* Evitar conflictos entre versiones de librerías
* Mantener el proyecto organizado
* Facilitar la instalación y ejecución del sistema

---

## ▶️ Instrucciones de ejecución

### 1️⃣ Clonar el repositorio

```bash
cd visual-voice
```

### 2️⃣ Crear el entorno virtual

```bash
python -m venv venv
```

### 3️⃣ Activar el entorno virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5️⃣ Ejecutar el sistema

*Actualmente el proyecto se encuentra en fase de prototipo, por lo que no existe un único archivo principal de ejecución. Se presentan módulos funcionales que demuestran la detección, interpretación y generación de audio.*

Una vez finalizado, al ejecutarse el sistema:

* Activará la cámara
* Detectará objetos en tiempo real
* Generará descripciones auditivas del entorno

📌 **Nota:** Es necesario contar con una cámara funcional y permisos de acceso para su correcto funcionamiento.

---

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

VISUAL-VOICE está diseñado como una herramienta de apoyo para personas con discapacidad visual, permitiéndoles reconocer su entorno inmediato a través de indicaciones auditivas. El sistema puede ser utilizado en interiores o exteriores, ayudando a identificar personas, obstáculos y elementos relevantes para una navegación más segura.

---

## 🛠️ Herramientas y tecnologías utilizadas

* **Lenguaje de programación:** Python
* **Visión artificial:** OpenCV
* **Modelo de detección:** YOLO (Ultralytics – v8)
* **Deep Learning:** PyTorch
* **Procesamiento semántico:** Reglas lógicas personalizadas
* **Lenguaje natural:** Plantillas de generación de texto
* **Text-to-Speech:** pyttsx3
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
* Definición de métricas de evaluación (precisión, latencia, usabilidad)
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

Como resultado, se obtuvo un sistema funcional capaz de detectar objetos en tiempo real, interpretar su ubicación y comunicar esta información al usuario mediante descripciones auditivas claras. VISUAL-VOICE demuestra el potencial de la inteligencia artificial aplicada a la accesibilidad, ofreciendo una solución viable, local y escalable para mejorar la autonomía de personas con discapacidad visual.

---

## 📌 Trabajo futuro

* Integración con dispositivos móviles
* Mejora en la estimación de distancias
* Inclusión de reconocimiento de texto (OCR) y señales
* Optimización del rendimiento en tiempo real
* Evaluaciones con usuarios finales

---

📍 *Proyecto desarrollado con fines académicos.*
