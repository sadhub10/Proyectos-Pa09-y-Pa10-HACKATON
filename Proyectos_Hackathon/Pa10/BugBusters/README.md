# ErgoVision 🧘💡💧
**ErgoVision** es una interfaz de bienestar que usa **visión artificial** para monitorear la **postura frente al computador** y el **nivel de iluminación** del entorno, con el objetivo de reducir fatiga visual y molestias musculares durante el estudio o trabajo.

> *Desarrollado por: Equipo BugBusters*  
> Joseph Batista: Desarrollador Backend
> Juan Castillo: Documentación
> Laura Rivera: Líder de grupo
> Marco Rodríguez: Desarrollador Frontend   
> © 2025 Samsung Innovation Campus | ErgoVision

Como mejora, el sistema incluye un módulo **beta de detección de hidratación**, capaz de identificar automáticamente el gesto de “tomar agua” y reiniciar el contador de hidratación.

---

## ✨ Funcionalidades principales

### ✅ Detección de postura (Frontal y Lateral)
- Clasificación de postura en **Buena / Regular / Mala**.
- Basada en **MediaPipe Pose** y ángulos del cuello.
- Alertas configurables por mala postura sostenida.

### ✅ Monitoreo de iluminación
- Estimación del brillo ambiental (escala **0–255**).
- Clasificación: **Buena / Regular / Mala iluminación**.
- Alertas por iluminación insuficiente.

### ✅ Hidratación (Modo Frontal – Beta)
- Detección del gesto de beber agua usando la distancia **muñeca → nariz** como proxy.
- Reinicio automático del temporizador al detectar hidratación.
- Visualización del estado:
  **“Hidratación detectada hace: X minutos (intervalo: Y min)”**
- Botón manual para registrar hidratación durante la demostración.

> Nota: esta funcionalidad es experimental y depende de la visibilidad de la mano y el rostro.

---

## 🧠 Tecnologías utilizadas
- **Python**
- **Streamlit**
- **streamlit-webrtc**
- **MediaPipe Pose**
- **OpenCV**
- **NumPy**

---

## 📦 Requisitos
- Python 3.9 o superior
- Webcam o cámara virtual (ej. DroidCam)

Dependencias:
```bash
pip install streamlit streamlit-webrtc opencv-python mediapipe numpy
```

---

## ▶️ Ejecución del proyecto
```bash
streamlit run proyecto_modulo_ia.py
```

---

## 🧭 Uso rápido
1. Ejecuta la aplicación.
2. Selecciona **Cámara lateral** o **Cámara frontal**.
3. Ajusta umbrales y alertas desde el sidebar.
4. En modo frontal:
   - Activa la hidratación.
   - Usa el botón **“Tomé agua”** o realiza el gesto de beber.

---

## ⚠️ Limitaciones
- La detección de hidratación puede fallar si:
  - El vaso tapa completamente la cara.
  - La mano sale del encuadre.
  - La iluminación es muy baja.
- El sistema es una herramienta de apoyo, no sustituye recomendaciones médicas.

---

## 🚀 Futuras mejoras
- Historial y estadísticas por sesión.
- Calibración personalizada por usuario.
- Detección de objetos (botella/vaso).
- Integración con pausas activas y ergonomía avanzada.

---

## 👤 Proyecto
**ErgoVision**  
Proyecto de visión artificial enfocado en bienestar y ergonomía frente al computador.  
Desarrollado como avance para hackatón / trabajo final.
