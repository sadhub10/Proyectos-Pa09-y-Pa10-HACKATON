# Mental Health Monitoring – (NLP + Risk + Chatbot + Audio)

## Nombre del Equipo: Los Terreneitors
## Integrantes
- Valeria Agrazal
- Linette Bonilla
- Amy Him
- Imanol Rodríguez
- Ricardo Solís

## Mejoras frente al módulo de IA

El proyecto evoluciona de un prototipo de clasificación básica a un sistema **modular y escalable**, incorporando:
- **Múltiples backends de IA**: Baseline (SVM + TF-IDF) y **Transformer (DistilBERT fine-tuned)**.
- **Métricas y evaluación del Transformer**, guardadas en `reports/metrics/transformer_metrics.json`.
- **Score de riesgo** basado en predicción + confianza, con **nivel de riesgo** (NORMAL / MEDIO / ALTO).
- **Persistencia de registros (logging)** para análisis posteriores (CSV) y visualización de tendencia.
- **Chatbot emocional** con flujo de conversación (estado), recomendaciones dinámicas y manejo de casos críticos.
- Arquitectura por módulos (`src/inference`, `src/models`, `src/chatbot`) para facilitar mantenimiento y extensión (ej. audio/multimodal).

---

## Planteamiento del problema

Después de la pandemia, el impacto en la salud mental se volvió más visible y frecuente, pero el acceso a apoyo profesional no siempre es inmediato, y el análisis manual de grandes volúmenes de texto (mensajes, encuestas, diarios, reportes) es lento y poco escalable. Este proyecto aborda la necesidad de contar con una herramienta que permita **detectar tempranamente señales emocionales relevantes en texto**, priorizar casos mediante un **score de riesgo**, y ofrecer una base para seguimiento y orientación inicial, sin reemplazar la atención clínica.

---

## Objetivos del proyecto

El proyecto busca construir un sistema que:
- Clasifique estados emocionales en texto (Ansiedad, Depresión, Estrés e Ideación suicida) usando modelos de NLP.
- Integre un **Transformer** entrenado para mejorar la comprensión contextual frente a enfoques tradicionales.
- Calcule un **score de riesgo** que permita priorizar casos y generar alertas.
- Muestre resultados en un **dashboard** con historial y tendencias.
- Mantenga un **chatbot** con flujo conversacional para acompañamiento básico y recomendaciones dinámicas.
- Permita una arquitectura modular para extenderse posteriormente a audio/multimodal si se desea.

---

## Herramientas utilizadas

- **Python 3.12**
- **Streamlit** (interfaz web)
- **Hugging Face Transformers + PyTorch** (DistilBERT fine-tuning e inferencia)
- **scikit-learn** (Baseline: SVM + TF-IDF)
- **pandas / numpy** (procesamiento y análisis)
- **plotly** (visualizaciones)
- **joblib** (carga/guardado de modelos)
- **librosa** (herramientas de audio)

---

## Resultado del proyecto

Se obtuvo una aplicación funcional que analiza texto en español o inglés, genera una predicción emocional con confidencias por categoría, calcula un **score de riesgo** y lo muestra en un dashboard con historial. Además, el sistema incluye un chatbot con estado conversacional (duración, detonante, soporte) y recomendaciones variables según la emoción detectada, con mensajes especiales para casos críticos.

---

## Requisitos e instalación

### 1) Instalar dependencias (requirements.txt)

Debes instalar las librerías del proyecto antes de ejecutar cualquier módulo:

```bash
pip install -r requirements.txt
