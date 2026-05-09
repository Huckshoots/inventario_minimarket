import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

PRODUCTOS_FILE = os.path.join(DATA_DIR, "productos.json")
MOVIMIENTOS_FILE = os.path.join(DATA_DIR, "movimientos_stock.json")
VENTAS_FILE = os.path.join(DATA_DIR, "ventas.json")


def asegurar_archivos():
    """Crea la carpeta data y los archivos JSON si no existen."""
    os.makedirs(DATA_DIR, exist_ok=True)
    for ruta in [PRODUCTOS_FILE, MOVIMIENTOS_FILE, VENTAS_FILE]:
        if not os.path.exists(ruta):
            guardar_json(ruta, [])


def cargar_json(ruta):
    """Carga una lista desde un archivo JSON local."""
    asegurar_archivos()
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, FileNotFoundError):
        guardar_json(ruta, [])
        return []


def guardar_json(ruta, datos):
    """Guarda una lista en un archivo JSON local."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
