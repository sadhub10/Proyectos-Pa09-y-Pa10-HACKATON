"""
Vista de lecciones de PiLearn
"""

import tkinter as tk
from .base_view import BaseView
from components import SimpleButton, ScrollableFrame



class LessonView(BaseView):
    """Vista para mostrar lecciones educativas"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.leccion_actual = None
        self.seccion_actual = 0  
    
    def crear(self):
        """Crear vista de lección"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
    
    def mostrar_leccion(self, leccion):
        """Mostrar una lección completa"""
        self.leccion_actual = leccion
        self._limpiar_contenido()  
        
        self.crear_header(leccion.titulo, 
                         f"⏱ {leccion.duracion_minutos} min | {leccion.dificultad.capitalize()}")
        
        self._crear_tabs()
        self.content_scroll = ScrollableFrame(self.frame)
        self.content_scroll.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.cambiar_seccion(0)
        
        botones = [
            {'text': '← ANTERIOR', 'command': self.seccion_anterior, 
             'style': 'secondary', 'size': 'small', 'side': 'left'},
            {'text': 'SIGUIENTE →', 'command': self.seccion_siguiente,
             'style': 'primary', 'size': 'small', 'side': 'left'},
        ]
        
        if self.controller.hay_siguiente_leccion():
            botones.append({
                'text': 'SIGUIENTE LECCIÓN →→', 'command': self.controller.siguiente_leccion,
                'style': 'success', 'size': 'normal', 'side': 'right'
            })
        else:
            botones.append({
                'text': 'COMENZAR EJERCICIOS ✓', 'command': self.controller.iniciar_ejercicios,
                'style': 'success', 'size': 'normal', 'side': 'right'
            })
        
        self.crear_footer(botones)
    
    def _crear_tabs(self):
        """Crear pestañas de navegación"""
        tabs_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        tabs_frame.pack(fill='x', padx=20, pady=10)
        
        self.tab_buttons = []
        tabs = [
            ("📖 TEORÍA", 'info'),
            ("💡 EJEMPLOS", 'success'),
            ("⭐ CONSEJOS", 'warning')
        ]
        
        for i, (texto, estilo) in enumerate(tabs):
            btn = SimpleButton(tabs_frame, text=texto,
                             command=lambda idx=i: self.cambiar_seccion(idx),
                             style=estilo, size='normal')
            btn.pack(side='left', padx=5)
            self.tab_buttons.append(btn)
    
    def cambiar_seccion(self, seccion):
        """Cambiar a una sección específica"""
        self.seccion_actual = seccion
        
        for i, btn in enumerate(self.tab_buttons):
            if i == seccion:
                btn.config(relief='solid', bd=2)
            else:
                btn.config(relief='flat', bd=0)
        
        frame = self.content_scroll.get_frame()
        for widget in frame.winfo_children():
            widget.destroy()
        
        if seccion == 0:
            self._mostrar_teoria(frame)
        elif seccion == 1:
            self._mostrar_ejemplos(frame)
        else:
            self._mostrar_consejos(frame)
    
    def _mostrar_teoria(self, parent):
        """Mostrar sección de teoría"""
        if not self.leccion_actual:
            return
        
        titulo_frame = tk.Frame(parent, bg='#E3F2FD', bd=2, relief='solid')
        titulo_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(titulo_frame, text="📖 CONTENIDO TEÓRICO",
                font=('Arial', 16, 'bold'),
                bg='#E3F2FD',
                fg=self.colors['info']).pack(pady=15)
        
        contenido = self.leccion_actual.contenido
        if contenido:
            text_frame = tk.Frame(parent, bg='white', bd=2, relief='sunken')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame,
                                font=('Arial', 10),
                                bg='white',
                                fg=self.colors['text_primary'],
                                wrap='word',
                                relief='flat',
                                padx=15, pady=15)
            text_widget.insert('1.0', contenido)
            text_widget.config(state='disabled')
            text_widget.pack(fill='both', expand=True)
    
    def _mostrar_ejemplos(self, parent):
        """Mostrar ejemplos prácticos"""
        if not self.leccion_actual or not self.leccion_actual.tiene_ejemplos():
            tk.Label(parent, text="No hay ejemplos disponibles",
                    font=('Arial', 10)).pack(pady=50)
            return
        
        titulo_frame = tk.Frame(parent, bg='#E8F5E9', bd=2, relief='solid')
        titulo_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(titulo_frame, text="💡 EJEMPLOS PRÁCTICOS",
                font=('Arial', 16, 'bold'),
                bg='#E8F5E9',
                fg=self.colors['success']).pack(pady=15)
        
        ejemplos = self.leccion_actual.ejemplos
        if ejemplos:
            text_frame = tk.Frame(parent, bg='white', bd=2, relief='sunken')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame,
                                font=('Courier', 10),
                                bg='#F0FFF0',
                                fg=self.colors['text_primary'],
                                wrap='word',
                                relief='flat',
                                padx=15, pady=15)
            text_widget.insert('1.0', ejemplos)
            text_widget.config(state='disabled')
            text_widget.pack(fill='both', expand=True)
    
    def _mostrar_consejos(self, parent):
        """Mostrar consejos y trucos"""
        if not self.leccion_actual or not self.leccion_actual.tiene_consejos():
            tk.Label(parent, text="No hay consejos disponibles",
                    font=('Arial', 10)).pack(pady=50)
            return
        
        titulo_frame = tk.Frame(parent, bg='#FFF9C4', bd=2, relief='solid')
        titulo_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(titulo_frame, text="⭐ CONSEJOS Y TRUCOS",
                font=('Arial', 16, 'bold'),
                bg='#FFF9C4',
                fg=self.colors['warning']).pack(pady=15)
        
        consejos = self.leccion_actual.consejos
        if consejos:
            text_frame = tk.Frame(parent, bg='white', bd=2, relief='sunken')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            text_widget = tk.Text(text_frame,
                                font=('Arial', 10),
                                bg='#FFFEF0',
                                fg=self.colors['text_primary'],
                                wrap='word',
                                relief='flat',
                                padx=15, pady=15)
            text_widget.insert('1.0', consejos)
            text_widget.config(state='disabled')
            text_widget.pack(fill='both', expand=True)
    
    def seccion_anterior(self):
        """Ir a sección anterior"""
        if self.seccion_actual > 0:
            self.cambiar_seccion(self.seccion_actual - 1)
    
    def seccion_siguiente(self):
        """Ir a sección siguiente"""
        if self.seccion_actual < 2:
            self.cambiar_seccion(self.seccion_actual + 1)
    
    def _limpiar_contenido(self):
        """Limpiar solo el contenido del frame, no las variables"""
        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()
        self.tab_buttons = []
    
    def limpiar(self):
        """Limpiar completamente la vista (cuando se cambia de pantalla)"""
        self._limpiar_contenido()
        self.leccion_actual = None
        self.seccion_actual = 0
        if hasattr(self, 'content_scroll'):
            delattr(self, 'content_scroll')
