"""
Controlador de ejercicios
"""

import random
from config import MAX_EXERCISES


class ExerciseController:
    """Controlador para manejo de ejercicios"""
    
    def __init__(self, app_controller, database, validador):
        self.app = app_controller
        self.db = database
        self.validador = validador
        
        self.materia_actual = None
        self.dificultad_actual = None
        self.ejercicios = []
        self.indice_actual = 0
        
        self.total_respondidos = 0
        self.correctas = 0
        self.incorrectas = 0
        self.puntos_totales = 0
    
    def iniciar(self, materia, dificultad):
        """Iniciar sesión de ejercicios"""
        self.materia_actual = materia
        self.dificultad_actual = dificultad
        
        self.ejercicios = self.db.obtener_ejercicios(materia, dificultad, MAX_EXERCISES)
        
        if not self.ejercicios:
            from tkinter import messagebox
            messagebox.showerror("Sin ejercicios",
                               f"No hay ejercicios disponibles para {materia} - {dificultad}")
            self.app.volver()
            return
        
        self.indice_actual = 0
        self.total_respondidos = 0
        self.correctas = 0
        self.incorrectas = 0
        self.puntos_totales = 0
        
        self.mostrar_ejercicio_actual()
    
    def mostrar_ejercicio_actual(self):
        """Mostrar el ejercicio actual"""
        if self.indice_actual < len(self.ejercicios):
            self.app.mostrar_vista('ejercicio')
            ejercicio = self.ejercicios[self.indice_actual]
            vista = self.app.vistas.get('ejercicio')
            if vista:
                vista.mostrar_ejercicio(
                    ejercicio,
                    self.indice_actual + 1,
                    len(self.ejercicios)
                )
    
    def verificar_respuesta(self, respuesta_usuario):
        """Verificar respuesta del usuario"""
        if self.indice_actual >= len(self.ejercicios):
            return
        
        ejercicio = self.ejercicios[self.indice_actual]
        
        es_correcta, confianza, mensaje = self.validador.validar_respuesta(
            respuesta_usuario,
            ejercicio.respuesta_correcta,
            ejercicio.materia
        )
        
        if not es_correcta and ejercicio.tiene_opciones_alternativas():
            alternativas = ejercicio.get_opciones_alternativas()
            for alternativa in alternativas:
                es_alt, conf_alt, msg_alt = self.validador.validar_respuesta(
                    respuesta_usuario,
                    alternativa,
                    ejercicio.materia
                )
                if es_alt:
                    es_correcta = True
                    confianza = conf_alt
                    mensaje = msg_alt
                    break
        
        self.total_respondidos += 1
        if es_correcta:
            self.correctas += 1
            self.puntos_totales += ejercicio.puntos
        else:
            self.incorrectas += 1
        
        vista = self.app.vistas.get('ejercicio')
        if vista:
            vista.mostrar_retroalimentacion(es_correcta, mensaje)
        
        print(f"📊 Respuesta: {'✓' if es_correcta else '✗'} | "
              f"Confianza: {confianza:.2%} | {mensaje}")
    
    def siguiente_ejercicio(self):
        """Avanzar al siguiente ejercicio"""
        self.indice_actual += 1
        
        if self.indice_actual < len(self.ejercicios):
            self.mostrar_ejercicio_actual()
        else:
            self.mostrar_resultados()
    
    def saltar_ejercicio(self):
        """Saltar ejercicio actual"""
        self.siguiente_ejercicio()
    
    def mostrar_resultados(self):
        """Mostrar resultados finales"""
        precision = (self.correctas / self.total_respondidos * 100) if self.total_respondidos > 0 else 0
        
        estadisticas = {
            'total': self.total_respondidos,
            'correctas': self.correctas,
            'incorrectas': self.incorrectas,
            'puntos': self.puntos_totales,
            'precision': precision
        }
        
        self.app.mostrar_resultados(estadisticas)
    
    def volver(self):
        """Volver al menú"""
        if self.total_respondidos > 0:
            from tkinter import messagebox
            confirmar = messagebox.askyesno(
                "Confirmar",
                "¿Deseas salir? Se perderá el progreso actual."
            )
            if confirmar:
                self.app.volver()
        else:
            self.app.volver()
