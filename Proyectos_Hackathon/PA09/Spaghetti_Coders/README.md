# SkillBridge IA

**Plataforma inteligente para la reinserción económica post pandemia y mejorar la empleabilidad**

---

## Equipo de desarrollo – *SPAGHETTI CODERS*🍝

* Ovidio Roberto Calderón Esquivel
* Diego Alexander Gordón Ruiz
* Chen Enrique Alex Fong Fan
* Anthony Praxedes Torres Silleros
* Lia Anyeline Cárdenas Berrio

---

## Descripción general

**SkillBridge IA** es una aplicación desarrollada en Python que utiliza técnicas de **Inteligencia Artificial y Procesamiento de Lenguaje Natural (NLP)** para analizar currículums, compararlos con vacantes laborales reales y generar **planes de mejora personalizados**, con el objetivo de apoyar la **reinserción económica post pandemia**.

El proyecto está orientado a reducir la brecha existente entre las habilidades de las personas desempleadas y los requerimientos actuales del mercado laboral, ofreciendo recomendaciones claras, accionables y basadas en datos.

---

## Problemática central

Tras la pandemia, una gran cantidad de personas se enfrenta a dificultades para reinsertarse en el mercado laboral debido a:

* Falta de claridad sobre cómo sus habilidades encajan en las vacantes disponibles.
* Desconocimiento de las habilidades específicas que el mercado está demandando.
* CVs mal estructurados o poco optimizados para sistemas de selección automatizados (ATS).
* Ausencia de orientación práctica sobre cómo mejorar su perfil profesional.

Este escenario provoca largos periodos de desempleo, subempleo y una desconexión entre talento disponible y necesidades reales de las empresas.

---

## Solución propuesta

SkillBridge IA aborda esta problemática mediante una solución integral basada en IA que:

1. Analiza automáticamente el contenido de un CV (PDF o DOCX).
2. Extrae habilidades, educación y datos clave usando NLP.
3. Compara semánticamente el perfil del candidato con vacantes reales mediante embeddings.
4. Identifica brechas de habilidades específicas para cada vacante.
5. Recomienda cursos relevantes para cerrar dichas brechas.
6. Evalúa la calidad del CV mediante un CV Score orientado a sistemas ATS.
7. Genera recomendaciones concretas para mejorar el CV y aumentar la empleabilidad.

Adicionalmente, el sistema ofrece un dashboard agregado para análisis de mercado desde la perspectiva empresarial.

---

## Impacto en el usuario

Antes de usar SkillBridge IA, el usuario:

* No sabe por qué no es seleccionado.
* No tiene claridad sobre qué habilidades le faltan.
* No cuenta con un plan concreto para mejorar su perfil.

Después de usar SkillBridge IA, el usuario:

* Comprende qué vacantes se ajustan mejor a su perfil.
* Identifica claramente las brechas que debe cerrar.
* Recibe recomendaciones específicas de cursos y mejoras para su CV.
* Aumenta su probabilidad de reinserción laboral de forma más rápida y dirigida.

---

## ¿Cómo funciona la IA?

1. **Lectura del CV (NLP)**
   Se extrae texto de archivos PDF/DOCX y se detectan datos clave y habilidades utilizando técnicas de NLP y listas de habilidades con sinónimos.

2. **Matching inteligente con embeddings**
   El CV y cada vacante se representan como vectores numéricos y se comparan usando similitud coseno para medir compatibilidad semántica.

3. **Análisis de brechas de habilidades**
   Se comparan las habilidades del candidato con las requeridas por cada vacante.

4. **Sistema de recomendación**
   Se sugieren cursos relevantes para reducir las brechas detectadas.

5. **Puntajes automáticos**
   Se calculan indicadores de empleabilidad y calidad del CV para apoyar la toma de decisiones.

Todo el procesamiento se realiza de forma local, sin el uso de APIs externas.

---

## Funcionalidades principales

### Para candidatos

* Análisis automático de CVs (PDF y DOCX)
* Extracción de habilidades y educación
* Matching con vacantes laborales
* Selección de vacante objetivo
* Detección de brechas de habilidades
* Recomendación de cursos
* CV Score y Employability Score
* Recomendaciones concretas para mejorar el CV

### Para empresas

* Análisis agregado de múltiples perfiles
* Identificación de habilidades más demandadas
* Detección de brechas comunes en candidatos
* Visualización de vacantes con mayor dificultad de cobertura
* Insights para planificación de capacitación y reclutamiento

---

## Tecnologías utilizadas

* Python 3.10
* Streamlit
* spaCy
* scikit-learn
* Pandas y NumPy
* pdfminer
* python-docx
* JSON como formato de datos

---

## Estructura del proyecto

```
skillbridge-ia/
│
├── app.py
├── data/
│   ├── skills.json
│   ├── jobs.json
│   ├── courses.json
│   └── demo_cvs/
│
├── src/
│   ├── resume_parser.py
│   ├── matching_embeddings.py
│   ├── gap_analysis.py
│   ├── recommender.py
│   ├── scoring.py
│   ├── cv_score.py
│   └── cv_coach.py
│
├── utils/
│   └── helpers.py
│
├── models/
│   └── embeddings 
│
└── README.md
```

---

## Cómo ejecutar el proyecto

```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm
streamlit run app.py
```

---

## Estado del proyecto

MVP funcional orientado a hackathon, con enfoque social y empresarial, listo para demostración y evaluación.
