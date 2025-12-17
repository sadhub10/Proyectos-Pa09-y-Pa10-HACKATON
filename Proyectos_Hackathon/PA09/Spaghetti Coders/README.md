#  SKILL BRIDGE IA

**Proyecto de análisis inteligente de perfiles profesionales (IA local)**

---

##  Equipo — *SPAGHETTI CODERS 🍝*

* **Ovidio Roberto Calderón Esquivel**
* **Diego Alexander Gordón Ruiz**
* **Chen Enrique Alex Fong Fan**
* **Anthony Praxedes Torres Silleros**
* **Lia Anyeline Cárdenas Berrio**

---

##  Descripción

**Skill Bridge IA** es una herramienta desarrollada en **Python** que utiliza **procesamiento de lenguaje natural (NLP) local** para analizar currículums y perfiles profesionales, con el objetivo de apoyar procesos de **evaluación y orientación laboral**.

El proyecto funciona de manera **completamente local**, sin uso de APIs externas ni servicios en la nube, priorizando la **privacidad de los datos** y la simplicidad de implementación.

---

##  Objetivo

Construir un motor de análisis que permita **extraer, analizar y comparar información profesional** a partir de currículums y datasets internos, como base para soluciones de reinserción laboral.

---

##  Funcionalidades actuales

* Lectura de currículums en formato **PDF y DOCX**
* Extracción de texto y datos relevantes
* Procesamiento de texto con **spaCy (NLP local)**
* Identificación de habilidades
* Comparación de habilidades con datasets internos
* Análisis básico de brechas de habilidades
* Sistema inicial de puntuación de perfiles

---

##  Tecnologías utilizadas

* **Python 3**
* **spaCy**
* **pdfminer.six**
* **python-docx**
* **Regex**
* **JSON**

>  No se utilizan APIs externas.

---

##  Estructura del proyecto

```text
SKILL_BRIDGE_IA/
│
├── data/
│   ├── courses.json
│   ├── jobs.json
│   └── skills.json
│
├── docs/
│
├── models/
│
├── src/
│   ├── gap_analysis.py
│   ├── recommender.py
│   ├── resume_parser.py
│   ├── scoring.py
│   └── skill_matcher.py
│
├── utils/
│   └── helpers.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

##  Ejecución básica

```bash
pip install -r requirements.txt
python app.py
```

---

##  Estado del proyecto

 **En desarrollo (núcleo funcional implementado)**

El proyecto cuenta con su lógica principal de análisis y comparación de perfiles en funcionamiento, sirviendo como base para futuras extensiones.


