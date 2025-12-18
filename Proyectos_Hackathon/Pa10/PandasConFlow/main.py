"""
PiLearn - Sistema Inteligente de Aprendizaje
Archivo principal de entrada

Ejecutar con: python main.py
"""

import tkinter as tk
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers import AppController


def main():
    """Función principal"""
    try:
        root = tk.Tk()
        app = AppController(root)
        
        print("✓ Interfaz gráfica iniciada\n")
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n\n⚠ Programa interrumpido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n ERROR FATAL: {e}")
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para salir...")
        sys.exit(1)


if __name__ == "__main__":
    main()
