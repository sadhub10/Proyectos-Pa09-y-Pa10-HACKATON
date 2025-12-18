#CODESCORE 
- Adriel Perez 7-714-275
- Sharon Correa 3-750-257
- Ernesto Yee 8-963-608
- Edgar Gonzales 8-1029-2276

# Predicción de Riesgo Financiero en Microempresas (15 días → cierre de mes)

Sistema de Machine Learning para estimar el riesgo financiero con datos de los primeros 15 días del mes y predecir cómo cerrará el mes (riesgo BAJO / MEDIO / ALTO). El proyecto busca funcionar como una alerta temprana para apoyar decisiones financieras y reducir pérdidas sostenidas.

---

## Tabla de contenido
- Descripción del proyecto
- Objetivo general
- Objetivos específicos
- Alcance
- Dataset
- Variables utilizadas
- Modelo y entrenamiento
- Métricas de evaluación
- Resultados (referencia)
- Estructura del repositorio
- Requisitos
- Instalación
- Ejecución del entrenamiento
- Guardar y cargar el modelo
- Uso del modelo (inferencia)
- Buenas prácticas (anti-leakage)
- Plan de interfaz (futuro)
- Integrantes
- Licencia

---

## Descripción del proyecto
Muchas microempresas presentan meses con ganancia y otros con pérdida. Cuando existe un mal manejo de ingresos, gastos y liquidez, estas variaciones pueden acumularse y derivar en problemas de sostenibilidad e incluso quiebra. Este proyecto propone un modelo predictivo que, a partir del desempeño financiero de los primeros 15 días, predice el riesgo al cierre del mes, permitiendo tomar acciones correctivas antes de finalizar el periodo.

---

## Objetivo general
Resolver las problemáticas que tienen las microempresas para evitar pérdidas sostenidas y riesgo de quiebra por mal manejo financiero, mediante la ayuda de un sistema inteligente para la detección temprana del riesgo de cierre mensual (BAJO, MEDIO o ALTO) a partir de datos financieros de los primeros 15 días del mes.

---

## Objetivos específicos
- Analizar el dataset para comprender distribución, calidad y consistencia de las variables financieras.
- Preparar un conjunto de datos apto para Machine Learning, con variables explicativas construidas únicamente con información de los primeros 15 días.
- Implementar un pipeline de preprocesamiento robusto para tratar valores faltantes, variables categóricas y escalado de variables numéricas cuando aplique.
- Entrenar un modelo de clasificación multiclase (BAJO / MEDIO / ALTO) que permita predecir el riesgo al cierre del mes.
- Evaluar el desempeño del modelo con métricas y visualizaciones estándar (matriz de confusión, ROC One-vs-Rest, reporte de clasificación).
- Exportar el modelo entrenado y su metadata para integrarlo posteriormente en una interfaz de usuario.

---

## Alcance
Incluye:
- Preparación y exploración de datos (EDA).
- Entrenamiento y evaluación de un modelo de clasificación multiclase.
- Exportación del modelo (pipeline completo) y archivos de metadata.
- Base técnica lista para integrarse a una interfaz.

No incluye (por ahora):
- Desarrollo completo de la interfaz final.
- Despliegue en producción.

---

## Dataset
El dataset está organizado por registros de tipo (empresa, mes) e incluye:
- Variables agregadas de los primeros 15 días del mes.
- Variables de cierre del mes.
- Etiqueta objetivo: riesgo_fin_mes.

---

## Variables utilizadas
Features (primeros 15 días):
- ingresos_15
- gastos_fijos_15
- gastos_variables_15
- gastos_totales_15
- ventas_15
- margen_ganancia_15
- liquidez_corriente_15

Target:
- riesgo_fin_mes {BAJO, MEDIO, ALTO}

---

## Modelo y entrenamiento
Modelo principal:
- RandomForestClassifier (Scikit-learn)

---

## Métricas de evaluación
- Accuracy
- Precision
- Recall
- F1-score
- Matriz de confusión
- ROC-AUC

---

## Resultados (referencia)
Buena separación entre clases BAJO y ALTO. La clase MEDIO suele ser la más compleja.

---

## Estructura del repositorio
Proyectos/
└── Codescore/
    └── Docmentacion/
    └── Recursos/
    └── Codigo/

---

## Requisitos
Python 3.9+, pandas, numpy, scikit-learn

---

## Instalación
pip install -r requirements.txt

---

## Integrantes
- Adriel Perez
- Sharon Correa
- Ernesto Yee
- Edgar Gonzales

---

## Licencia
Proyecto académico.
