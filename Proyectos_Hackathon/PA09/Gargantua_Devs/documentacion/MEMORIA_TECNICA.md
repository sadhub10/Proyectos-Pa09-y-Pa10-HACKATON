

## 1. Visión General
El proyecto consiste en el desarrollo de un ecosistema de Inteligencia Artificial diseñado para la predicción de la incidencia criminal (homicidios) en la República de Panamá. El sistema trasciende los modelos estadísticos tradicionales al integrar una arquitectura híbrida que correlaciona el historial delictivo con indicadores socioeconómicos dinámicos, permitiendo una visión prospectiva del riesgo social a nivel provincial.

## 2. Arquitectura de Datos y Pipeline ETL
El sistema se fundamenta en la integración de fuentes de datos heterogéneas mediante un pipeline de procesamiento robusto:
* **Ingesta:** Unificación de registros históricos del Ministerio Público ($2017-2024$) y proyecciones socioeconómicas oficiales.
* **Aumento de Datos (Data Augmentation):** Implementación de un motor de generación de contexto que simula variables de desempleo, densidad poblacional e índice de actividad de grupos delictivos, ajustado a hitos históricos como el impacto económico de la pandemia $COVID-19$.
* **Normalización:** Estandarización de entidades geográficas y temporales para garantizar la integridad referencial en el cruce de variables exógenas.

## 3. Ingeniería de Características (Feature Engineering)
La capacidad predictiva del modelo se basa en un vector de entrada de $9$ dimensiones, destacando:
* **Componentes Autorregresivos (Lags):** Captura de la inercia criminal inmediata ($Mes_{t-1}$).
* **Análisis de Tendencia (Rolling Window):** Cálculo de medias móviles trimestrales para suavizar el ruido estadístico mensual.
* **Métrica de Volatilidad Estocástica:** Introducción de una métrica de desviación estándar móvil para cuantificar el grado de incertidumbre y varianza en zonas específicas, mejorando la respuesta del modelo ante picos atípicos de violencia (*outliers*).

## 4. Especificaciones del Modelo de Aprendizaje Automático
Se implementó un algoritmo de **Random Forest Regressor** bajo las siguientes optimizaciones de ingeniería:
* **Ensamblaje:** $300$ estimadores (árboles de decisión) para garantizar la estabilidad de la predicción y reducir la varianza.
* **Regularización:** Aplicación de *Cost-Complexity Pruning* ($\text{ccp\_alpha}=0.015$) para prevenir el sobreajuste y asegurar la capacidad de generalización en datos no observados.
* **Validación:** Partición de datos mediante *Hold-out validation* con una semilla de aleatoriedad fija para garantizar la reproducibilidad científica de los resultados.

## 5. Resultados y Métricas de Desempeño
El modelo final ($V4.1$) presenta un equilibrio óptimo entre precisión y robustez operativa:
* **Coeficiente de Determinación ($R^{2}$):** $76.41\%$, indicando una alta capacidad para explicar la varianza de los fenómenos criminales.
* **Error Absoluto Medio (MAE):** $1.97$, manteniendo la desviación promedio por debajo de los $2$ incidentes por unidad de tiempo/espacio.
* **Índice de Robustez (Gap):** Diferencia controlada entre los puntajes de entrenamiento y prueba de $5.1\%$, validando la ausencia de memorización (*overfitting*).

## 6. Conclusión de Despliegue
La solución se integra mediante una interfaz interactiva desarrollada en **Streamlit**, la cual permite la parametrización en tiempo real y la visualización de niveles de riesgo (Bajo, Medio, Alto). El sistema actúa como una herramienta técnica de apoyo a la toma de decisiones estratégicas en políticas de seguridad pública y prevención ciudadana.

---
**Gargantua Devs | Hackathon Samsung Innovation Campus 2025**

