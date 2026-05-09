"""
Sistema de Gestión de Inventario - MiniMarket Express
Versión modular con Python + Tkinter + JSON.

Ejecución:
    python main.py

No usa SQLite ni otra base de datos. Los datos se guardan en la carpeta data/.
"""

import tkinter as tk
from storage.json_storage import asegurar_archivos
from ui.app import InventarioApp


if __name__ == "__main__":
    asegurar_archivos()
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()
