"""
Modelo de ejercicio
"""


class Exercise:
    """Representa un ejercicio educativo"""
    
    def __init__(self, data):
        """
        Inicializar ejercicio desde tupla de BD
        
        Args:
            data: tupla con datos del ejercicio
        """
        self.id = data[0]
        self.pregunta = data[1]
        self.respuesta_correcta = data[2]
        self.retroalimentacion = data[3]
        self.dificultad = data[4]
        self.categoria = data[5]
        self.materia = data[6] if len(data) > 6 else 'matematicas'
        self.pista1 = data[7] if len(data) > 7 else "Piensa paso a paso"
        self.pista2 = data[8] if len(data) > 8 else "Revisa los conceptos básicos"
        self.pista3 = data[9] if len(data) > 9 else "No te rindas, puedes lograrlo"
        self.puntos = data[10] if len(data) > 10 else 10
        self.tiempo_estimado = data[11] if len(data) > 11 else 60
        self.opciones = data[12] if len(data) > 12 else ""
    
    def get_pistas(self):
        """Obtener lista de pistas"""
        return [self.pista1, self.pista2, self.pista3]
    
    def get_opciones_alternativas(self):
        """Obtener lista de respuestas alternativas válidas"""
        if not self.opciones:
            return []
        return [opt.strip() for opt in self.opciones.split('|')]
    
    def tiene_opciones_alternativas(self):
        """Verificar si tiene respuestas alternativas"""
        return bool(self.opciones)
    
    def __repr__(self):
        return f"Exercise(id={self.id}, materia={self.materia}, dificultad={self.dificultad})"
