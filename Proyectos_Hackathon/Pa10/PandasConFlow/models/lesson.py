"""
Modelo de lección
"""


class Lesson:
    """Representa una lección educativa"""
    
    def __init__(self, data):
        """
        Inicializar lección desde tupla de BD
        
        Args:
            data: tupla con datos de la lección
        """
        self.id = data[0]
        self.titulo = data[1]
        self.materia = data[2]
        self.dificultad = data[3]
        self.categoria = data[4]
        self.contenido = data[5]
        self.ejemplos = data[6] if len(data) > 6 else ""
        self.consejos = data[7] if len(data) > 7 else ""
        self.duracion_minutos = data[8] if len(data) > 8 else 10
        self.orden = data[9] if len(data) > 9 else 0
    
    def tiene_ejemplos(self):
        """Verificar si tiene ejemplos"""
        return bool(self.ejemplos and self.ejemplos.strip())
    
    def tiene_consejos(self):
        """Verificar si tiene consejos"""
        return bool(self.consejos and self.consejos.strip())
    
    def get_secciones_contenido(self):
        """Obtener secciones del contenido"""
        if not self.contenido:
            return []
        return [s.strip() for s in self.contenido.split('\n\n') if s.strip()]
    
    def get_ejemplos_lista(self):
        """Obtener lista de ejemplos"""
        if not self.tiene_ejemplos():
            return []
        return [e.strip() for e in self.ejemplos.split('\n\n') if e.strip() and '===' not in e and '---' not in e]
    
    def __repr__(self):
        return f"Lesson(id={self.id}, titulo={self.titulo}, materia={self.materia})"
