# 🦺 AI Safety Inspector

**AI Safety Inspector** es una aplicación web interactiva desarrollada con **Streamlit** y **YOLOv8** que utiliza visión por computadora para **detectar Equipos de Protección Personal (EPP)** en imágenes de sitios de trabajo y evaluar el **nivel de cumplimiento de seguridad laboral**.

El proyecto está orientado a entornos como **construcción, manufactura, minería y logística**, donde el uso adecuado de EPP es crítico para la prevención de accidentes.

---

## 🚀 Características Principales

* 📸 Análisis de imágenes de sitios de trabajo
* 🎯 Detección automática de EPP (cascos, chalecos, personas)
* 📊 Dashboard interactivo con métricas y visualizaciones
* ✅ Cálculo de score de seguridad en tiempo real
* 🎨 Interfaz moderna y amigable
* 📈 Gráficos interactivos con Plotly

---

## 🧠 ¿Cómo Funciona?

1. El usuario sube una imagen del sitio de trabajo.
2. El modelo **YOLOv8** detecta personas y elementos de seguridad.
3. El sistema evalúa si los trabajadores cumplen con el uso de EPP.
4. Se genera un **score de seguridad** y un dashboard con estadísticas.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10 – 3.11 (recomendado)**
* **Streamlit** – Interfaz web
* **YOLOv8 (Ultralytics)** – Detección de objetos
* **OpenCV** – Procesamiento de imágenes
* **Plotly** – Visualizaciones interactivas
* **Pandas** – Manejo de datos
* **NumPy** – Cálculo numérico
* **Pillow (PIL)** – Manejo de imágenes

---

## 📂 Estructura del Proyecto

```
ai-safety-inspector/
│
├── app.py                # Aplicación principal Streamlit
├── best.pt               # (Opcional) Modelo YOLO entrenado personalizado
├── yolov8n.pt            # Modelo YOLO base
├── requirements.txt      # Dependencias principales
├── README.md             # Documentación
└── myenv/                # Entorno virtual (opcional)
```

---

## ⚙️ Instalación y Ejecución

> ⚠️ **IMPORTANTE:** Usa Python **3.10 o 3.11**. Python 3.14 NO es compatible con PyTorch y Pillow.

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/ai-safety-inspector.git
cd ai-safety-inspector
```

### 2️⃣ Crear entorno virtual

```bash
python3.11 -m venv myenv
source myenv/bin/activate  # Linux / macOS
# myenv\\Scripts\\activate  # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4️⃣ Instalar PyTorch (PASO CLAVE)

#### CPU

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### GPU NVIDIA (CUDA 12.1)

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 5️⃣ Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador.

---

## 📊 Dashboard de Seguridad

El dashboard incluye:

* Número total de objetos detectados
* Score global de seguridad (%)
* Estado de uso de casco y chaleco
* Gráfico de detecciones por tipo
* Gráfico de nivel de confianza por detección
* Indicador tipo **Gauge** de seguridad

---

## 🧪 Modelo de Detección

* Por defecto se utiliza **YOLOv8n** preentrenado.
* Si existe un archivo `best.pt`, el sistema lo carga automáticamente como modelo personalizado.
* Se recomienda entrenar el modelo con datasets específicos de EPP para mayor precisión.

📌 Dataset sugerido:

* *Hard Hat Detection Dataset (Kaggle)*

---

## 📈 Cálculo del Score de Seguridad

* Si se detectan personas:

  * Se evalúa el uso de casco y chaleco.
  * **Score = (EPP detectado / EPP requerido) × 100**
* Si no hay personas:

  * Score = **100%**

---

## 🔐 Limitaciones

* Solo analiza imágenes (no video en tiempo real aún).
* Depende de la calidad y el ángulo de la imagen.
* El modelo base puede no detectar todos los tipos de EPP.

---

## 🧩 Próximas Mejoras

* 🎥 Detección en video en tiempo real
* 🚨 Alertas automáticas de riesgo
* 🗄️ Integración con bases de datos
* 📄 Exportación de reportes en PDF
* 📡 Integración con cámaras IP

---

## 👨‍💻 Autor

Proyecto desarrollado como **demo / hackathon 2025** enfocado en el uso de **IA aplicada a la seguridad laboral**.

---

## 📜 Licencia

Este proyecto se distribuye bajo la licencia **MIT**.

Eres libre de usarlo, modificarlo y adaptarlo.

---

## 💡 Nota Final

> *La inteligencia artificial no reemplaza la supervisión humana, pero puede ser una poderosa aliada para salvar vidas.*

🦺 **Trabajemos por entornos laborales más seguros.**
