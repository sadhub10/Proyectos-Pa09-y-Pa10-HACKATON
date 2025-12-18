"""
Constantes globales de PiLearn
"""

# Configuración de ventana
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 600

# Configuración de ejercicios
MAX_EXERCISES = 30

# Base de datos
DB_PATH = "pitutor_raspberry.db"

# Umbrales de validación ML
THRESHOLDS = {
    'exact_match': 1.0,
    'fuzzy_high': 0.97,
    'fuzzy_good': 0.90,
    'fuzzy_acceptable': 0.80,
    'semantic_high_short': 0.60,
    'semantic_high_long': 0.65,
    'semantic_low_short': 0.30,
    'semantic_low_long': 0.35,
    'combined_high_short': 0.45,
    'combined_high_long': 0.50,
    'combined_low_short': 0.35,
    'combined_low_long': 0.38,
}

# Configuración de materias
MATERIAS = ['matematicas', 'ingles', 'programacion']
DIFICULTADES = ['basico', 'intermedio', 'avanzado']

# Mapeo de nombres para display
MATERIA_NOMBRES = {
    'matematicas': 'Matemáticas',
    'ingles': 'Inglés',
    'programacion': 'Programación'
}

DIFICULTAD_NOMBRES = {
    'basico': 'Básico',
    'intermedio': 'Intermedio',
    'avanzado': 'Avanzado'
}
