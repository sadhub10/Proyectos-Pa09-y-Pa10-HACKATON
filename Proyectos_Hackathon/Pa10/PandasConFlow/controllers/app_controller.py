"""
Controlador principal de la aplicación PiLearn
"""

import tkinter as tk
from models import Database, ValidadorInteligente
from views import MainMenuView, LessonView, ExerciseView, ResultsView
from .lesson_controller import LessonController
from .exercise_controller import ExerciseController
from config import WINDOW_WIDTH, WINDOW_HEIGHT, DB_PATH


class AppController:
    """Controlador principal de la aplicación"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PiLearn - Sistema Inteligente de Aprendizaje")
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)  
        self.root.minsize(800, 600)  
        
        self.db = Database(DB_PATH)
        self.validador = ValidadorInteligente()
        
        self.lesson_controller = LessonController(self, self.db)
        self.exercise_controller = ExerciseController(self, self.db, self.validador)
        
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill='both', expand=True)
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        self.vistas = {}
        self.vista_actual = None
        
        self._inicializar()
    
    def _inicializar(self):
        """Inicializar la aplicación"""
        print("\n" + "="*50)
        print("  PiLearn - Sistema Inteligente de Aprendizaje")
        print("="*50 + "\n")
        
        exito, mensaje = self.db.inicializar()
        if not exito:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error inicializando BD:\n{mensaje}")
            return
        
        print(f"✓ Base de datos lista: {mensaje}\n")
        
        self.vistas['menu'] = MainMenuView(self.main_container, self)
        self.vistas['leccion'] = LessonView(self.main_container, self.lesson_controller)
        self.vistas['ejercicio'] = ExerciseView(self.main_container, self.exercise_controller)
        self.vistas['resultados'] = ResultsView(self.main_container, self)
        
        self.mostrar_vista('menu')
    
    def mostrar_vista(self, nombre):
        """Cambiar a una vista específica"""
        for child in self.main_container.winfo_children():
            try:
                child.pack_forget()
            except Exception:
                pass
            try:
                child.place_forget()
            except Exception:
                pass

        if nombre not in self.vistas:
            return

        for key, vista in self.vistas.items():
            if not vista.frame:
                vista.crear()

        for key, vista in self.vistas.items():
            if key == nombre:
                vista.mostrar()
            else:
                vista.ocultar()

        self.vista_actual = nombre
    
    def seleccionar_materia_dificultad(self, materia, dificultad):
        """Usuario selecciona materia y dificultad"""
        lecciones = self.db.obtener_lecciones(materia, dificultad)
        
        if lecciones:
            self._mostrar_opciones_estudio(materia, dificultad, lecciones)
        else:
            self.exercise_controller.iniciar(materia, dificultad)
            self.mostrar_vista('ejercicio')
    
    def _mostrar_opciones_estudio(self, materia, dificultad, lecciones):
        """Mostrar opciones: aprender primero o practicar directo"""
        from tkinter import Toplevel
        from components import SimpleButton
        from config import COLORS
        
        dialog = Toplevel(self.root)
        dialog.title("¿Cómo quieres comenzar?")
        dialog.geometry("600x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="¿Cómo quieres empezar?",
                font=('Arial', 16, 'bold'),
                bg=COLORS['card']).pack(pady=20)
        
        opciones_frame = tk.Frame(dialog, bg=COLORS['bg_primary'])
        opciones_frame.pack(expand=True, fill='both', padx=30, pady=20)
        
        leccion_frame = tk.Frame(opciones_frame, bg='white', bd=2, relief='solid')
        leccion_frame.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(leccion_frame, text="APRENDER PRIMERO",
                font=('Arial', 12, 'bold'),
                bg='white').pack(pady=10)
        
        tk.Label(leccion_frame, text=f"{len(lecciones)} lecciones disponibles",
                font=('Arial', 10),
                bg='white').pack()
        
        SimpleButton(leccion_frame, text="VER LECCIONES",
                    command=lambda: [dialog.destroy(), 
                                   self.lesson_controller.iniciar(materia, dificultad, lecciones),
                                   self.mostrar_vista('leccion')],
                    style='info').pack(pady=20)
        
        practica_frame = tk.Frame(opciones_frame, bg='white', bd=2, relief='solid')
        practica_frame.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(practica_frame, text="PRACTICAR DIRECTO",
                font=('Arial', 12, 'bold'),
                bg='white').pack(pady=10)
        
        ejercicios_count = self.db.contar_ejercicios(materia, dificultad)
        tk.Label(practica_frame, text=f"{ejercicios_count} ejercicios disponibles",
                font=('Arial', 10),
                bg='white').pack()
        
        SimpleButton(practica_frame, text="INICIAR EJERCICIOS",
                    command=lambda: [dialog.destroy(),
                                   self.exercise_controller.iniciar(materia, dificultad),
                                   self.mostrar_vista('ejercicio')],
                    style='success').pack(pady=20)
    
    def contar_ejercicios(self, materia, dificultad):
        """Contar ejercicios disponibles"""
        return self.db.contar_ejercicios(materia, dificultad)
    
    def volver(self):
        """Volver al menú principal"""
        self.mostrar_vista('menu')
    
    def mostrar_resultados(self, estadisticas):
        """Mostrar pantalla de resultados"""
        self.vistas['resultados'].mostrar_resultados(estadisticas)
        self.mostrar_vista('resultados')
    
    def ir_menu_principal(self):
        """Ir al menú principal"""
        self.mostrar_vista('menu')
    
    def practicar_de_nuevo(self):
        """Practicar de nuevo con la misma configuración"""
        if hasattr(self.exercise_controller, 'materia_actual'):
            self.exercise_controller.iniciar(
                self.exercise_controller.materia_actual,
                self.exercise_controller.dificultad_actual
            )
            self.mostrar_vista('ejercicio')
        else:
            self.mostrar_vista('menu')
