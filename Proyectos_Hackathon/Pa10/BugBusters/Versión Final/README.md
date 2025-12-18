# 🧠💻 ErgoVision  
### Asistente inteligente para ergonomía, iluminación e hidratación frente al computador

**ErgoVision** es un sistema inteligente desarrollado para mejorar los hábitos de trabajo frente al computador, combinando **visión por computadora**, **análisis temporal** y **notificaciones inteligentes**.  
El proyecto actúa como un *manager de ergonomía*, ayudando al usuario a mantener una postura adecuada, trabajar con buena iluminación y desarrollar hábitos saludables de hidratación, mientras registra su progreso a lo largo del tiempo.

---

## 🎯 Objetivo del proyecto

Promover **hábitos saludables y sostenibles** durante jornadas prolongadas frente al computador mediante:
- Retroalimentación en tiempo real  
- Alertas preventivas inteligentes  
- Registro histórico del comportamiento del usuario  

---

## 🚀 Funcionalidades principales

### 🧍‍♂️ Monitoreo de postura (modo frontal y lateral)
- Detección del ángulo del cuello usando landmarks corporales.
- Clasificación continua de la postura:
  - **Buena**
  - **Regular**
  - **Mala**
- Alertas automáticas al mantener mala postura durante un tiempo configurable.
- Lógica independiente para cámara **frontal** y **lateral**.

---

### 💡 Evaluación de la iluminación
- Análisis en tiempo real del nivel de brillo del entorno.
- Clasificación del ambiente:
  - Buena
  - Regular
  - Baja
- Alertas cuando la iluminación es insuficiente.
- Registro del tiempo acumulado en cada estado.

---

### 💧 Hidratación inteligente (sistema unificado)
- Un único sistema de hidratación compartido entre ambos modos.
- Registro de hidratación mediante:
  - 🖐️ **Detección automática del gesto de beber** (muñeca → boca).
  - ✅ **Botón manual “Tomé agua”** desde la interfaz.
- Intervalo configurable entre recordatorios.
- Notificaciones cuando el usuario excede el tiempo recomendado sin hidratarse.
- Conteo de eventos de hidratación por sesión.

---

### ⏱️ Tiempo sentado / tiempo de trabajo frente al computador

ErgoVision **mide el tiempo sentado del usuario**, definido técnicamente como:

> **Tiempo de monitoreo activo frente al computador**

Este tiempo corresponde al período en el que:
- La cámara está activa  
- El usuario está siendo analizado (postura + iluminación)

Este enfoque evita ambigüedades y permite medir de forma precisa el **tiempo efectivo de trabajo frente al computador**.

El tiempo se:
- Acumula automáticamente durante la sesión
- Almacena como `duration_sec`
- Visualiza en minutos en el historial
- Utiliza para métricas globales y análisis de hábitos

---

### 🔔 Sistema de alertas y notificaciones
- Alertas configurables para:
  - Mala postura
  - Iluminación deficiente
  - Falta de hidratación
- Notificaciones de escritorio.
- Sistema de *cooldown* para evitar alertas repetitivas.
- Sonido opcional configurable.

---

## 📈 Historial y análisis por sesiones

ErgoVision registra **una fila por sesión**, sin almacenar video ni imágenes (privacidad del usuario).

### 📦 Base de datos
- Motor: **SQLite**
- Archivo generado automáticamente: `ergovision_sessions.db`

### 📊 Métricas registradas por sesión
- Duración total de la sesión (tiempo sentado)
- Tiempo acumulado por:
  - Postura buena / regular / mala
  - Iluminación buena / regular / baja
- Puntajes (0–100):
  - Postura
  - Iluminación
- Número de alertas enviadas
- Eventos de hidratación
- Promedio de minutos entre bebidas

### 📉 Visualización
- Tabla detallada por sesión
- KPIs generales:
  - Número de sesiones
  - Tiempo total monitoreado
  - Promedios de postura e iluminación
- Gráficas de tendencia por sesión

---

## 🗂️ Estructura del proyecto

```
ErgoVision/
│
├── ErgoVision_main.py      # Aplicación principal (Streamlit)
├── common.py               # Lógica compartida y callbacks de visión
├── sidebar_config.py       # Configuración global y controles
├── mode_frontal.py         # Análisis con cámara frontal
├── mode_lateral.py         # Análisis con cámara lateral
├── notificaciones.py       # Sistema de notificaciones
├── session_logger.py       # Persistencia en SQLite
├── history_view.py         # Visualización del historial
├── ergovision_sessions.db  # Base de datos (auto-generada)
└── README.md
```

---

## ⚙️ Tecnologías utilizadas
- Python 3.10+
- Streamlit
- streamlit-webrtc
- OpenCV
- MediaPipe
- SQLite
- Pandas

---

## ▶️ Ejecución del proyecto

```bash
pip install streamlit streamlit-webrtc opencv-python mediapipe pandas
streamlit run ErgoVision_main.py
```

Permite el acceso a la cámara para el correcto funcionamiento.

---

## 🧪 Estado del proyecto
- ✔️ Funcional y estable para demo y hackathon  
- ✔️ Arquitectura modular y escalable  
- ✔️ Historial persistente por sesión  
- ⚠️ Detección de gesto de hidratación en fase beta  
- ❌ No se almacenan imágenes ni video (privacidad)

---

## 👥 Equipo de desarrollo

**Desarrollado por:**  
**Equipo BugBusters**

- **Joseph Batista** – Desarrollador Backend  
- **Juan Castillo** – Documentación  
- **Laura Rivera** – Líder de Equipo  
- **Marco Rodríguez** – Desarrollador Frontend  

---

© **2025 Samsung Innovation Campus | ErgoVision**
