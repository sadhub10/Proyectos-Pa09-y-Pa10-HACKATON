"""
Controlador de lecciones
"""


class LessonController:
    """Controlador para manejo de lecciones"""
    
    def __init__(self, app_controller, database):
        self.app = app_controller
        self.db = database
        
        self.materia_actual = None
        self.dificultad_actual = None
        self.lecciones = []
        self.indice_actual = 0
    
    def iniciar(self, materia, dificultad, lecciones=None):
        """Iniciar modo de lecciones"""
        self.materia_actual = materia
        self.dificultad_actual = dificultad
        
        if lecciones:
            self.lecciones = lecciones
        else:
            self.lecciones = self.db.obtener_lecciones(materia, dificultad)
        
        self.indice_actual = 0
        
        if self.lecciones:
            self.mostrar_leccion_actual()
    
    def mostrar_leccion_actual(self):
        """Mostrar la lección actual"""
        if 0 <= self.indice_actual < len(self.lecciones):
            self.app.mostrar_vista('leccion')
            leccion = self.lecciones[self.indice_actual]
            vista_leccion = self.app.vistas.get('leccion')
            if vista_leccion:
                vista_leccion.mostrar_leccion(leccion)
    
    def siguiente_leccion(self):
        """Avanzar a la siguiente lección"""
        self.indice_actual += 1
        
        if self.indice_actual < len(self.lecciones):
            self.mostrar_leccion_actual()
        else:
            from tkinter import messagebox
            messagebox.showinfo("Lecciones completadas",
                              "¡Has completado todas las lecciones!\n\n" +
                              "Ahora vamos a practicar con ejercicios.")
            self.iniciar_ejercicios()
    
    def leccion_anterior(self):
        """Retroceder a la lección anterior"""
        if self.indice_actual > 0:
            self.indice_actual -= 1
            self.mostrar_leccion_actual()
    
    def hay_siguiente_leccion(self):
        """Verificar si hay más lecciones"""
        return self.indice_actual < len(self.lecciones) - 1
    
    def iniciar_ejercicios(self):
        """Iniciar ejercicios después de las lecciones"""
        self.app.exercise_controller.iniciar(
            self.materia_actual,
            self.dificultad_actual
        )
        self.app.mostrar_vista('ejercicio')
    
    def volver(self):
        """Volver al menú"""
        self.app.volver()
