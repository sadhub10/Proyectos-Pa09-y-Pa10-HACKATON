"""
Vista base para todas las pantallas de PiLearn
"""

import tkinter as tk
from config import COLORS


class BaseView:
    """Clase base para todas las vistas"""
    
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.colors = COLORS
        self.frame = None
    
    def crear(self):
        """Crear la vista (debe ser implementado por subclases)"""
        raise NotImplementedError("Las subclases deben implementar crear()")
    
    def mostrar(self):
        """Mostrar la vista"""
        if self.frame:
            self.frame.grid(row=0, column=0, sticky='nsew')
            self.frame.tkraise()
    
    def ocultar(self):
        """Ocultar la vista"""
        if self.frame:
            try:
                self.frame.grid_remove()
            except Exception:
                pass
            try:
                self.frame.pack_forget()
            except Exception:
                pass
            try:
                self.frame.place_forget()
            except Exception:
                pass
    
    def destruir(self):
        """Destruir la vista"""
        if self.frame:
            self.frame.destroy()
            self.frame = None
    
    def limpiar(self):
        """Limpiar contenido de la vista"""
        if self.frame:
            for widget in self.frame.winfo_children():
                widget.destroy()
    
    def crear_header(self, titulo, subtitulo=None, mostrar_boton_volver=True):
        """Crear header estándar para las vistas"""
        header_frame = tk.Frame(self.frame, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        
        content = tk.Frame(header_frame, bg=self.colors['primary'])
        content.pack(fill='x', padx=20, pady=12)
        
        if mostrar_boton_volver:
            from components import SimpleButton
            SimpleButton(content, text="← VOLVER",
                        command=self.controller.volver,
                        style='secondary',
                        size='small').pack(side='left')
        
        tk.Label(content, text=titulo,
                font=('Arial', 20, 'bold'),
                bg=self.colors['primary'],
                fg='white').pack(side='left', padx=30)
        
        if subtitulo:
            tk.Label(content, text=subtitulo,
                    font=('Arial', 10),
                    bg=self.colors['primary'],
                    fg='white').pack(side='right')
        
        return header_frame
    
    def crear_footer(self, botones=None):
        """Crear footer con botones"""
        footer_frame = tk.Frame(self.frame, bg=self.colors['bg_primary'])
        footer_frame.pack(fill='x', side='bottom', padx=20, pady=10)
        
        if botones:
            for boton_config in botones:
                from components import SimpleButton
                side = boton_config.pop('side', 'left')
                btn = SimpleButton(footer_frame, **boton_config)
                btn.pack(side=side, padx=5)
        
        return footer_frame
    
    def mostrar_mensaje(self, titulo, mensaje, tipo='info'):
        """Mostrar mensaje al usuario"""
        from tkinter import messagebox
        
        if tipo == 'info':
            messagebox.showinfo(titulo, mensaje)
        elif tipo == 'warning':
            messagebox.showwarning(titulo, mensaje)
        elif tipo == 'error':
            messagebox.showerror(titulo, mensaje)
        elif tipo == 'question':
            return messagebox.askyesno(titulo, mensaje)
