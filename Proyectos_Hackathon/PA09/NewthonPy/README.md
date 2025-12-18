# SAMSUNG-INNOVATION-CAMPUS-HACKATHON
# CSV AI Analyzer - Analizador Inteligente de CSV

## Descripción

Aplicación web inteligente que utiliza IA para analizar automáticamente archivos CSV, detectar su tipo (finanzas, ventas, gastos, rendimiento, etc.), realizar análisis avanzados y comparar múltiples archivos para encontrar patrones y tendencias.


## Integrantes

- **Aula**: PA09
- **Nombre del equipo**: Newton.py

### Integrantes del equipo:

1. Isaac Delgado
2. Milagros Alonzo
3. Sebastián Rodriguez
4. Carlos Roseman
5. Liseth Abrego


## Características Principales

- **Detección Automática**: La IA detecta automáticamente el tipo de CSV y su estructura
- **Análisis Inteligente**: Análisis profundo adaptado al tipo de datos
- **Visualizaciones Dinámicas**: Gráficos interactivos generados automáticamente
- **Comparación Multi-CSV**: Compara archivos similares de diferentes períodos
- **Chatbot Inteligente**: Pregunta sobre los datos analizados
- **Clasificación Automática**: Clasifica CSVs por categorías (finanzas, ventas, RRHH, etc.)

## 🏗️ Estructura del Proyecto

```
csv-ai-analyzer/
├── backend/                     # API Backend con FastAPI
│   ├── app/
│   │   ├── main.py             # API principal
│   │   ├── models/             # Modelos de datos
│   │   ├── services/           # Lógica de negocio
│   │   │   ├── csv_analyzer.py # Analizador de CSV
│   │   │   ├── ai_classifier.py# Clasificador con IA
│   │   │   └── chatbot.py      # Chatbot inteligente
│   │   └── utils/              # Utilidades
│   └── requirements.txt
├── frontend/                    # Frontend con React
│   ├── src/
│   │   ├── components/         # Componentes reutilizables
│   │   ├── pages/              # Páginas principales
│   │   ├── services/           # Servicios API
│   │   └── App.jsx             # App principal
│   └── package.json
└── README.md
```


## 📖 Cómo Usar

1. **Subir CSV**: Arrastra archivos CSV o haz clic para seleccionar
2. **Análisis Automático**: La IA detecta el tipo y analiza los datos
3. **Ver Resultados**: Explora gráficos, estadísticas y insights
4. **Comparar**: Sube múltiples archivos para comparaciones
5. **Chat**: Haz preguntas sobre los datos analizados

## Ejemplos

### Gastos Operativos
```
La IA detectará: "CSV de Gastos Operativos"
Análisis: Gastos por departamento, tendencias, proveedores frecuentes
```

### Ventas/Rendimiento
```
La IA detectará: "CSV de Rendimiento de Empleados"
Análisis: Top performers, ventas promedio, efectividad
```


## Tipos de CSV Soportados

- ✅ Gastos operativos
- ✅ Ventas y rendimiento
- ✅ Datos de empleados (RRHH)
- ✅ Inventarios
- ✅ Finanzas
- ✅ Y cualquier otro tipo (la IA se adapta CASI JEJEJE)

## próximas Funcionalidades que esperamos incluir 

- [ ] Exportar reportes en PDF
- [ ] Alertas automáticas
- [ ] mejorar chatbot
- [ ] Dashboard personalizable 

