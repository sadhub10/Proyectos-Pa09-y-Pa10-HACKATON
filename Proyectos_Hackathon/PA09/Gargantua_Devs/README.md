# 🇵🇦 Predicción de Riesgo de Criminalidad: Enfoque Socioeconómico y Temporal
**Equipo:** Gargantua Devs
**Aulas:** PA09 / PA10

## 📄 Descripción del Proyecto
Herramienta de Inteligencia Artificial diseñada para analizar y predecir la incidencia de homicidios en Panamá. A diferencia de los modelos tradicionales lineales, nuestra solución implementa un **Random Forest Regressor** optimizado que integra:
1.  **Lag Features (Series Temporales):** Inercia criminal histórica.
2.  **Variables Socioeconómicas:** Tasa de desempleo (impacto post-pandemia), densidad poblacional e índice de pandillas.

## 🚀 Innovación Técnica y Robustez


* **Algoritmo:** Random Forest con *Cost-Complexity Pruning* (`ccp_alpha=0.015`).
* **Optimización:** Búsqueda de hiperparámetros (Grid Search) con 200 iteraciones y validación cruzada temporal.
* **Resultado:** Se logró una **brecha (gap) de apenas 1.4%** entre entrenamiento y pruebas, eliminando el *overfitting* y garantizando predicciones realistas.

## 🛠️ Estructura del Código
* **`app.py`**: Interfaz interactiva en Streamlit. Carga automáticamente el contexto socioeconómico según la provincia y año seleccionado.
* **`Entrenamiento_Modelo.ipynb`**: Notebook con el flujo completo: Limpieza -> Ingeniería de Características -> Entrenamiento "Ultra" -> Validación.

## 📋 Instrucciones de Ejecución Local
1.  Clonar el repositorio y navegar a la carpeta del proyecto.
2.  Instalar dependencias:
    ```bash
    pip install -r codigo/requirements.txt
    ```
3.  Ejecutar la aplicación (asegúrese de estar en la raíz de la carpeta del equipo):
    ```bash
    streamlit run codigo/app.py
    ```

## 📊 Fuentes de Datos
* **Homicidios:** Ministerio Público (Datos Abiertos 2017-2024).
* **Contexto:** INEC (Proyecciones de Población y Desempleo) e Insight Crime (Índice de Pandillas).
