"""
Vista de ejercicios de PiLearn
"""

import tkinter as tk
from .base_view import BaseView
from components import SimpleButton, SimpleEntry, ProgressBar


class ExerciseView(BaseView):
    """Vista para practicar ejercicios"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.ejercicio_actual = None
        self.pista_actual = 0
        self.entry = None
    
    def crear(self):
        """Crear vista de ejercicio"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
    
    def mostrar_ejercicio(self, ejercicio, numero, total):
        """Mostrar un ejercicio"""
        self.ejercicio_actual = ejercicio
        self.pista_actual = 0
        self.retro_frame = None 
        self._limpiar_contenido()
        
        self.crear_header("Ejercicio en Progreso", 
                         f"Ejercicio {numero}/{total}")
        
        progress_container = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        progress_container.pack(fill='x', padx=20, pady=10)
        
        self.progress_bar = ProgressBar(progress_container, width=800, height=20)
        self.progress_bar.pack()
        self.progress_bar.set_progress(numero / total)
        
        pregunta_frame = tk.Frame(self.frame, bg='white', bd=2, relief='solid')
        pregunta_frame.pack(fill='both', expand=True, padx=40, pady=20)
        
        tk.Label(pregunta_frame,
                text=ejercicio.pregunta,
                font=('Arial', 16, 'bold'),
                bg='white',
                fg=self.colors['text_primary'],
                wraplength=800,
                justify='left').pack(pady=30, padx=30)
        
        respuesta_container = tk.Frame(pregunta_frame, bg='white')
        respuesta_container.pack(pady=20)
        
        tk.Label(respuesta_container, text="Tu respuesta:",
                font=('Arial', 10),
                bg='white').pack(anchor='w', padx=30)
        
        self.entry = SimpleEntry(respuesta_container, width=50)
        self.entry.pack(padx=30, pady=10)
        self.entry.focus()
        self.entry.bind_key('<Return>', lambda e: self.verificar_respuesta())
        
        botones_frame = tk.Frame(pregunta_frame, bg='white')
        botones_frame.pack(pady=20)
        
        SimpleButton(botones_frame, text="💡 PISTA",
                    command=self.mostrar_pista,
                    style='warning',
                    size='normal').pack(side='left', padx=5)
        
        SimpleButton(botones_frame, text="✓ VERIFICAR",
                    command=self.verificar_respuesta,
                    style='success',
                    size='normal').pack(side='left', padx=5)
        
        SimpleButton(botones_frame, text="➜ SALTAR",
                    command=self.controller.siguiente_ejercicio,
                    style='secondary',
                    size='normal').pack(side='left', padx=5)
        
        self.pistas_container = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        self.pistas_container.pack(fill='x', padx=40, pady=10)
    
    def mostrar_pista(self):
        """Mostrar siguiente pista"""
        if not self.ejercicio_actual:
            return
        
        if hasattr(self, 'retro_frame') and self.retro_frame:
            return
        
        pistas = self.ejercicio_actual.get_pistas()
        
        if self.pista_actual >= len(pistas):
            self.mostrar_mensaje("Sin más pistas", 
                               "Ya has usado todas las pistas disponibles",
                               'info')
            return
        
        pista = pistas[self.pista_actual]
        self.pista_actual += 1
        
        pista_frame = tk.Frame(self.pistas_container, bg='#FFF9C4', 
                              bd=2, relief='solid')
        pista_frame.pack(fill='x', pady=5)
        
        tk.Label(pista_frame,
                text=f"💡 Pista {self.pista_actual}: {pista}",
                font=('Arial', 10),
                bg='#FFF9C4',
                fg=self.colors['text_primary'],
                wraplength=800,
                justify='left',
                padx=15, pady=10).pack(fill='x')
    
    def verificar_respuesta(self):
        """Verificar respuesta del usuario"""
        if not self.ejercicio_actual or not self.entry:
            return
        
        respuesta = self.entry.get().strip()
        
        if not respuesta:
            self.mostrar_mensaje("Respuesta vacía",
                               "Por favor escribe una respuesta",
                               'warning')
            return
        
        self.entry.entry.config(state='disabled')
        
        
        self.controller.verificar_respuesta(respuesta)
    
    def mostrar_retroalimentacion(self, es_correcta, mensaje):
        """Mostrar retroalimentación de la respuesta"""
        if hasattr(self, 'retro_frame') and self.retro_frame:
            self.retro_frame.destroy()
        
        color = self.colors['success'] if es_correcta else self.colors['error']
        icono = "✓ ✓" if es_correcta else "✗"
        
        self.retro_frame = tk.Frame(self.frame, bg=color, bd=2, relief='solid')
        self.retro_frame.pack(fill='x', padx=40, pady=10)
        
        tk.Label(self.retro_frame,
                text=f"{icono} {mensaje}",
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white',
                padx=20, pady=15).pack()
        
        if es_correcta and self.ejercicio_actual:
            tk.Label(self.retro_frame,
                    text=self.ejercicio_actual.retroalimentacion,
                    font=('Arial', 10),
                    bg='white',
                    fg=self.colors['text_primary'],
                    wraplength=800,
                    justify='left',
                    padx=20, pady=10).pack(fill='x')
        
        if es_correcta:
            btn = SimpleButton(self.retro_frame, text="CONTINUAR → (Presiona Enter)",
                        command=self.controller.siguiente_ejercicio,
                        style='primary',
                        size='large')
            btn.pack(pady=15)
            self.retro_frame.bind('<Return>', lambda e: self.controller.siguiente_ejercicio())
            self.retro_frame.focus_set()
        else:
            botones_frame = tk.Frame(self.retro_frame, bg=color)
            botones_frame.pack(pady=15)
            
            SimpleButton(botones_frame, text="INTENTAR DE NUEVO",
                        command=self._reintentar,
                        style='warning',
                        size='normal').pack(side='left', padx=5)
            
            SimpleButton(botones_frame, text="CONTINUAR →",
                        command=self.controller.siguiente_ejercicio,
                        style='secondary',
                        size='normal').pack(side='left', padx=5)
    
    def _reintentar(self):
        """Permitir reintentar el ejercicio"""

        if hasattr(self, 'retro_frame') and self.retro_frame:
            self.retro_frame.destroy()
            self.retro_frame = None
        
        if self.entry:
            self.entry.entry.config(state='normal')
            self.entry.clear()
            self.entry.focus()
    
    def _limpiar_contenido(self):
        """Limpiar solo el contenido del frame"""
        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()
        if hasattr(self, 'retro_frame'):
            self.retro_frame = None
    
    def limpiar(self):
        """Limpiar completamente la vista de ejercicios (cuando se cambia de pantalla)"""
        self._limpiar_contenido()
        self.ejercicio_actual = None
        self.pista_actual = 0
        self.entry = None
        if hasattr(self, 'pregunta_label'):
            delattr(self, 'pregunta_label')
        if hasattr(self, 'pistas_container'):
            delattr(self, 'pistas_container')
        if hasattr(self, 'progress_bar'):
            delattr(self, 'progress_bar')
