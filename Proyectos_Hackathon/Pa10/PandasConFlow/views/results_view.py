"""
Vista de resultados de PiLearn
"""

import tkinter as tk
from .base_view import BaseView
from components import SimpleButton, Card


class ResultsView(BaseView):
    """Vista para mostrar resultados"""
    
    def crear(self):
        """Crear vista de resultados"""
        self.frame = tk.Frame(self.parent, bg=self.colors['bg_primary'])
    
    def mostrar_resultados(self, estadisticas):
        """
        Mostrar resultados de la sesión
        
        Args:
            estadisticas: dict con {total, correctas, incorrectas, puntos, precision}
        """
        self.limpiar()
        
        contenedor_central = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        contenedor_central.pack(expand=True, fill='both')
        
        header_frame = tk.Frame(contenedor_central, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        
        tk.Label(header_frame, text="¡Sesión Completada!",
                font=('Arial', 20, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(pady=12)
        
        precision = estadisticas.get('precision', 0)
        mensaje = self._get_mensaje_motivacional(precision)
        
        tk.Label(contenedor_central,
                text=mensaje,
                font=('Arial', 14, 'bold'),
                bg=self.colors['bg_primary'],
                fg=self.colors['text_primary']).pack(pady=15)
        
        stats_container = tk.Frame(contenedor_central, bg=self.colors['bg_primary'])
        stats_container.pack(fill='x', padx=60, pady=15)
        
        self._crear_card_estadistica(stats_container, "✓ Correctas",
                                     estadisticas.get('correctas', 0),
                                     self.colors['success'])
        
        self._crear_card_estadistica(stats_container, "✗ Incorrectas",
                                     estadisticas.get('incorrectas', 0),
                                     self.colors['error'])
        
        self._crear_card_estadistica(stats_container, "📊 Total",
                                     estadisticas.get('total', 0),
                                     self.colors['info'])
        
        precision_frame = tk.Frame(contenedor_central, bg=self.colors['primary'],
                                  bd=2, relief='solid')
        precision_frame.pack(fill='x', padx=100, pady=15)
        
        tk.Label(precision_frame,
                text=f"{precision:.1f}%",
                font=('Arial', 42, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(pady=8)
        
        tk.Label(precision_frame,
                text="Precisión",
                font=('Arial', 14, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(pady=3)
        
        tk.Label(precision_frame,
                text=f"⭐ {estadisticas.get('puntos', 0)} puntos obtenidos",
                font=('Arial', 10),
                bg=self.colors['primary'],
                fg='white').pack(pady=8)
        
        botones_frame = tk.Frame(contenedor_central, bg=self.colors['bg_primary'])
        botones_frame.pack(pady=15)
        
        SimpleButton(botones_frame, text='🏠 MENÚ PRINCIPAL',
                    command=self.controller.ir_menu_principal,
                    style='primary', size='large').pack(side='left', padx=10)
        
        SimpleButton(botones_frame, text='🔄 PRACTICAR DE NUEVO',
                    command=self.controller.practicar_de_nuevo,
                    style='success', size='large').pack(side='left', padx=10)
    
    def _crear_card_estadistica(self, parent, titulo, valor, color):
        """Crear card de estadística"""
        card = tk.Frame(parent, bg=color, bd=2, relief='raised')
        card.pack(side='left', expand=True, fill='both', padx=10)
        
        tk.Label(card,
                text=str(valor),
                font=('Arial', 36, 'bold'),
                bg=color,
                fg='white').pack(pady=20)
        
        tk.Label(card,
                text=titulo,
                font=('Arial', 12, 'bold'),
                bg=color,
                fg='white').pack(pady=10)
    
    def _get_mensaje_motivacional(self, precision):
        """Obtener mensaje motivacional según precisión"""
        if precision >= 90:
            return "🌟 ¡EXCELENTE! ¡Eres un maestro!"
        elif precision >= 70:
            return "🎉 ¡MUY BIEN! Vas por buen camino"
        elif precision >= 50:
            return "👍 ¡BIEN HECHO! Sigue practicando"
        else:
            return "💪 ¡SIGUE INTENTANDO! La práctica hace al maestro"
    
    def limpiar(self):
        """Limpiar vista de resultados"""
        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()
