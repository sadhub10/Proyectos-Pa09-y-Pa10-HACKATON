

## 📄 Descripción del Proyecto

A diferencia de los modelos de pronóstico convencionales, este no solo analiza el historial de crímenes, sino que interpreta el contexto humano. Nuestra solución utiliza un **Random Forest Regressor ** optimizado para detectar patrones de criminalidad basados en:

* **Inercia Temporal (Lag Features):** Análisis del comportamiento del mes anterior y tendencias trimestrales.
* **Métrica de Volatilidad Estocástica:** Capacidad del modelo para identificar zonas de alta varianza o "caos", permitiendo predicciones más estables.
* **Vectores Socioeconómicos Reales:** Integración de tasas de desempleo (incluyendo el impacto post-pandemia), proyecciones de densidad poblacional y actividad de pandillas por región.



## 📁 Estructura del Repositorio



* **codigo/**
    * `app.py`: Interfaz interactiva para el usuario final (Streamlit).
    * `pipeline_entrenamiento.ipynb`: Flujo completo de ciencia de datos con celdas de salida pre-ejecutadas.
    * `generador_contexto.py`: Script de ingeniería de datos para la creación de variables socioeconómicas.
    * `requirements.txt`: Lista de dependencias del entorno.
* **recursos/**
    * `modelo_homicidios_panama_socioeconomico_ULTRA.pkl`: Modelo serializado (binario).
    * `Dataset_Homicidios_Panama_2017_2024_NormalizadoFINAL.xlsx`: Base de datos histórica de crímenes.
    * `Datos_Contexto_Anual_MEJORADO.csv`: Dataset enriquecido de variables sociales.
* **documentacion/**
    * `README.md`: Documentación principal.

## 🛠️ Instrucciones de Ejecución Local

1.  **Clonación:** Clonar el repositorio y posicionarse en la carpeta del equipo.
2.  **Entorno Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Dependencias:**
    ```bash
    pip install -r codigo/requirements.txt
    ```
4.  **Lanzamiento:**
    ```bash
    streamlit run codigo/app.py
    ```

