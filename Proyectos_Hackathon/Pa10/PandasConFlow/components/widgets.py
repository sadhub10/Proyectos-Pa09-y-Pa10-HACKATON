"""
Componentes UI reutilizables para PiLearn
"""

import tkinter as tk
from config import COLORS


class SimpleButton(tk.Button):
    """Botón optimizado para Raspberry Pi"""
    
    def __init__(self, parent, text="", command=None, style='primary', size='normal', **kwargs):
        styles = {
            'primary': {
                'bg': COLORS['primary'],
                'fg': 'white',
                'active_bg': COLORS['primary_dark']
            },
            'success': {
                'bg': COLORS['success'],
                'fg': 'white',
                'active_bg': '#229954'
            },
            'warning': {
                'bg': COLORS['warning'],
                'fg': 'white',
                'active_bg': '#D68910'
            },
            'error': {
                'bg': COLORS['error'],
                'fg': 'white',
                'active_bg': '#CD6155'
            },
            'secondary': {
                'bg': COLORS['bg_secondary'],
                'fg': COLORS['text_primary'],
                'active_bg': COLORS['border']
            },
            'info': {
                'bg': COLORS['info'],
                'fg': 'white',
                'active_bg': '#2E86C1'
            }
        }
        
        sizes = {
            'small': {'padx': 12, 'pady': 6, 'font': ('Arial', 9)},
            'normal': {'padx': 16, 'pady': 8, 'font': ('Arial', 10, 'bold')},
            'large': {'padx': 20, 'pady': 10, 'font': ('Arial', 12, 'bold')}
        }
        
        style_config = styles.get(style, styles['primary'])
        size_config = sizes.get(size, sizes['normal'])
        
        default_config = {
            'text': text,
            'command': command,
            'font': size_config['font'],
            'bg': style_config['bg'],
            'fg': style_config['fg'],
            'activebackground': style_config['active_bg'],
            'activeforeground': style_config['fg'],
            'bd': 1,
            'relief': 'solid',
            'cursor': 'hand2',
            'padx': size_config['padx'],
            'pady': size_config['pady']
        }
        
        default_config.update(kwargs)
        super().__init__(parent, **default_config)


class SimpleEntry(tk.Frame):
    """Campo de entrada simple"""
    
    def __init__(self, parent, width=None, **kwargs):
        super().__init__(parent, bg=COLORS['card'])
        
        entry_config = {
            'font': ('Arial', 10),
            'bg': 'white',
            'fg': COLORS['text_primary'],
            'bd': 2,
            'relief': 'sunken'
        }
        if width:
            entry_config['width'] = width
        
        self.entry = tk.Entry(self, **entry_config)
        self.entry.pack(fill='both', expand=True, padx=8, pady=6)
    
    def get(self):
        return self.entry.get()
    
    def set(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value))
    
    def clear(self):
        self.entry.delete(0, tk.END)
    
    def focus(self):
        self.entry.focus()
    
    def bind_key(self, key, callback):
        self.entry.bind(key, callback)


class SimpleFrame(tk.Frame):
    """Frame simple con estilo consistente"""
    
    def __init__(self, parent, **kwargs):
        default_config = {
            'bg': COLORS['card'],
            'bd': 1,
            'relief': 'solid'
        }
        default_config.update(kwargs)
        super().__init__(parent, **default_config)


class Card(tk.Frame):
    """Tarjeta con sombra y estilos"""
    
    def __init__(self, parent, title=None, **kwargs):
        super().__init__(parent, bg=COLORS['card'], 
                        bd=2, relief='raised')
        
        if title:
            header = tk.Label(self, text=title, 
                            font=('Arial', 12, 'bold'),
                            bg=COLORS['primary'],
                            fg='white',
                            padx=15, pady=10)
            header.pack(fill='x')
        
        self.content = tk.Frame(self, bg=COLORS['card'])
        self.content.pack(fill='both', expand=True, padx=15, pady=15)
    
    def get_content(self):
        return self.content


class ProgressBar(tk.Canvas):
    """Barra de progreso personalizada"""
    
    def __init__(self, parent, width=400, height=20, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=COLORS['bg_secondary'],
                        highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self._progress = 0.0
    
    def set_progress(self, value):
        """Establecer progreso (0.0 - 1.0)"""
        self._progress = max(0.0, min(1.0, value))
        self._draw()
    
    def _draw(self):
        """Dibujar barra"""
        self.delete('all')
        fill_width = int(self.width * self._progress)
        
        self.create_rectangle(0, 0, fill_width, self.height,
                            fill=COLORS['success'],
                            outline='')
        
        self.create_rectangle(fill_width, 0, self.width, self.height,
                            fill=COLORS['bg_secondary'],
                            outline='')
        
        self.create_rectangle(0, 0, self.width, self.height,
                            outline=COLORS['border'],
                            width=1)


class ScrollableFrame(tk.Frame):
    """Frame con scroll automático"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['card'])
        
        self.canvas = tk.Canvas(self, bg=COLORS['card'],
                               highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                     command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, 
                                        bg=COLORS['card'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, 
                                 anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def get_frame(self):
        """Obtener el frame scrollable"""
        return self.scrollable_frame
