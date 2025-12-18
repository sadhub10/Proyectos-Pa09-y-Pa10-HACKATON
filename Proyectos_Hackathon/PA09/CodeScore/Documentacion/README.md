# 📊 MicroFinRisk  
### Sistema Predictivo de Riesgo Financiero para Microempresas en Panamá  
**Equipo:** CodeScore – Samsung Innovation Campus 2025  

---

## 📌 Descripción General  
**MicroFinRisk** es un sistema inteligente diseñado para **predecir de forma temprana el riesgo financiero de microempresas**, utilizando información correspondiente a los **primeros 15 días del mes** para estimar cómo cerrará el periodo (riesgo **BAJO, MEDIO o ALTO**).

El proyecto surge ante una problemática real:  
> Muchas microempresas no cuentan con herramientas que les permitan evaluar su situación financiera a tiempo, lo que provoca pérdidas sostenidas y cierres negativos por falta de planificación.

MicroFinRisk funciona como una **herramienta de alerta temprana**, facilitando decisiones oportunas sobre gastos, cobranza y liquidez.

---

## 🧠 Tecnologías y Modelos Utilizados  

### **Inteligencia Artificial**  
- **Random Forest Classifier (supervisado):**  
  Modelo entrenado con indicadores financieros para clasificar el riesgo financiero de cierre mensual en niveles bajo, medio o alto.  
- Uso de variables financieras clave y persistencia del modelo mediante **Joblib**.  
- Reglas de negocio complementarias para reforzar la interpretación del riesgo.

### **Backend – Python**  
- Pandas, NumPy, Joblib  
- Manejo de archivos CSV como base de datos  
- Procesamiento de métricas financieras y predicciones  

### **Frontend – Flet**  
- Interfaz gráfica organizada por pestañas  
- Formularios financieros interactivos  
- Dashboard de usuario y vista administrativa  

---

## 🚀 Funcionalidades Principales  

### 👤 **Modo Empresa (Usuario)**  
- Registro de información financiera de los primeros 15 días del mes  
- Visualización de indicadores financieros  
- Predicción del riesgo de cierre mensual  
- Gráficas y recomendaciones automáticas  

### 🛡️ **Modo Administrador**  
- Acceso protegido  
- Gestión de empresas y registros  
- Eliminación de datos por mes o año  

---

## 🌎 Impacto Social y Beneficios  
- Anticipación de problemas financieros  
- Apoyo a la toma de decisiones sin conocimientos contables avanzados  
- Reducción de pérdidas y cierres negativos  
- Democratización del análisis financiero mediante IA  

---

## 📁 Estructura del Proyecto  

```
CodeScore/
├── Codigo/
│   ├── main.py
│   ├── backend_microempresas.py
│
├── Recursos/
│   ├── data/
│   │   ├── empresas.csv
│   │   ├── registros_15d.csv
│   │   └── predicciones.csv
│   ├── artifacts/
│   │   └── modelo_random_forest.joblib
│   └── logo.png
│
├── Entrenamiento.ipynb
├── README.md
```

---

## 🛠️ Instalación y Ejecución  

### 1. Clonar el repositorio  
```bash
git clone https://github.com/sadhub10/SIC-2025-Aulas-Pa09-y-Pa10.git
```

### 2. Entrar al proyecto  
```bash
cd "SIC-2025-Aulas-Pa09-y-Pa10/Proyectos IA/Pa09/CodeScore"
```

### 3. Instalar dependencias  
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación  
```bash
python Codigo/main.py
```

---

## 👥 Equipo de Desarrollo – CodeScore  

| Nombre            | Rol                                    |
|-------------------|----------------------------------------|
| Adriel Pérez      | Coordinación y Entrenamiento de Modelos |
| Ernesto Yee      | Backend y Documentación                |
| Sharon Correa     | Desarrollo Frontend (Flet)             |
| Edgard González   | Documentación y QA                     |
