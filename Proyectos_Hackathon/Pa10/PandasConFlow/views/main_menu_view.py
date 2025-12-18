"""
Vista del menú principal de PiLearn
"""

import tkinter as tk
from .base_view import BaseView
from components import SimpleButton, Card
from config import MATERIA_NOMBRES, DIFICULTAD_NOMBRES


class MainMenuView(BaseView):
    """Vista del menú principal"""
    
    def crear(self):
        """Crear menú principal"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
        
        self._crear_logo()
        
        tk.Label(self.frame,
                text="Selecciona una materia y nivel de dificultad para comenzar",
                font=('Arial', 16, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_secondary']).pack(pady=(20, 30))
        
        opciones_container = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        opciones_container.pack(expand=True, fill='both', padx=50, pady=20)
        
        self._crear_cards_materias(opciones_container)
    
    def _crear_logo(self):
        """Crear logo y título de la aplicación"""
        logo_frame = tk.Frame(self.frame, bg=self.colors['primary'], 
                             height=120)
        logo_frame.pack(fill='x')
        logo_frame.pack_propagate(False)
        
        tk.Label(logo_frame,
                text="🎓 PiLearn",
                font=('Arial', 32, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(pady=20)
        
        tk.Label(logo_frame,
                text="Sistema Inteligente de Aprendizaje",
                font=('Arial', 10),
                bg=self.colors['primary'],
                fg='white').pack()
    
    def _crear_cards_materias(self, parent):
        """Crear tarjetas de materias"""
        materias = [
            ('matematicas', '📐', self.colors['info']),
            ('ingles', '🌍', self.colors['success']),
            ('programacion', '💻', self.colors['warning'])
        ]
        
        for materia, emoji, color in materias:
            card = Card(parent)
            card.pack(side='left', expand=True, fill='both', padx=10)
            
            content = card.get_content()
            
            tk.Label(content, text=emoji,
                    font=('Arial', 48),
                    bg=self.colors['card']).pack(pady=10)

            tk.Label(content, text=MATERIA_NOMBRES[materia],
                    font=('Arial', 16, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text_primary']).pack(pady=5)

            for dificultad in ['basico', 'intermedio', 'avanzado']:
                btn = SimpleButton(content,
                                  text=DIFICULTAD_NOMBRES[dificultad],
                                  command=lambda m=materia, d=dificultad: 
                                         self.controller.seleccionar_materia_dificultad(m, d),
                                  style='primary' if dificultad == 'basico' else 
                                        'success' if dificultad == 'intermedio' else 'warning',
                                  size='normal')
                btn.pack(pady=5, fill='x', padx=20)
                
                cantidad = self.controller.contar_ejercicios(materia, dificultad)
                tk.Label(content, 
                        text=f"{cantidad} ejercicios disponibles",
                        font=('Arial', 9),
                        bg=self.colors['card'],
                        fg=self.colors['text_muted']).pack()
    
    def limpiar(self):
        """Limpiar vista del menú"""
        pass
