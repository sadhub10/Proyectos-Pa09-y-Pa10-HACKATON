#CODESCORE 
 - Adriel Perez 7-714-275
 - Sharon Correa 3-750-257
 - Ernesto Yee 8-963-608
 - Edgar Gonzales 

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
- Desarrollo completo de la interfaz final (panel de captura, dashboard, administración).
- Despliegue en producción (servidor, contenedores o hosting).

---

## Dataset
El dataset está organizado por registros de tipo (empresa, mes) e incluye:
- Variables agregadas de los primeros 15 días del mes (features).
- Variables de cierre del mes (targets), utilizadas solo para entrenamiento y evaluación.
- Etiqueta objetivo: riesgo_fin_mes.

Nota sobre datos sintéticos:
En contexto universitario y por limitaciones de cantidad de datos reales, se puede incorporar un conjunto de datos sintéticos basado en relaciones financieras coherentes (ingresos, gastos, margen y liquidez), manteniendo rangos y patrones plausibles para entrenar y validar el modelo.

---

## Variables utilizadas
Features (solo primeros 15 días, ejemplos típicos):
- ingresos_15
- gastos_fijos_15
- gastos_variables_15
- gastos_totales_15
- ventas_15
- margen_ganancia_15
- liquidez_corriente_15
- Contexto opcional si existe: rubro, provincia, mes, anio/periodo

Target (cierre de mes):
- riesgo_fin_mes en {BAJO, MEDIO, ALTO}

---

## Modelo y entrenamiento
Modelo principal:
- RandomForestClassifier (Scikit-learn), configurado para clasificación multiclase y con balance de clases cuando aplique.

Pipeline de entrenamiento:
- Imputación de valores faltantes:
  - Numéricas: mediana
  - Categóricas: valor más frecuente
- Codificación de categóricas:
  - OneHotEncoder con manejo de categorías desconocidas
- Entrenamiento del modelo dentro de un Pipeline para garantizar reproducibilidad

Estrategia de partición:
- Preferencia por split temporal si existen columnas de periodo (anio/mes o periodo), simulando el uso real del sistema.
- En caso de no contar con periodo, se realiza train_test_split estratificado para mantener proporciones de clases.

Validación:
- Cross-validation (por ejemplo, 5-fold) usando F1 macro como métrica recomendada para multiclase.

---

## Métricas de evaluación
Se reportan métricas completas para clasificación multiclase:
- Accuracy
- Balanced Accuracy
- Precision (macro)
- Recall (macro)
- F1-score (macro y weighted)
- MCC (Matthews Correlation Coefficient)
- Cohen’s Kappa
- Log Loss
- ROC-AUC One-vs-Rest (cuando sea posible)
- Matriz de confusión
- Curvas ROC por clase (One-vs-Rest)

Además, se recomienda adjuntar:
- Classification report (precision, recall, f1 por clase)
- Gráficas de matriz de confusión y ROC

---

## Resultados (referencia)
Usualmente, los modelos presentan:
- Buena separación entre las clases BAJO y ALTO.
- La clase MEDIO tiende a ser la más compleja por representar una zona intermedia con características compartidas con ambos extremos.

Los resultados finales dependen del tamaño, calidad y representatividad del dataset (real y/o sintético).

---

## Estructura del repositorio
Ejemplo sugerido:
