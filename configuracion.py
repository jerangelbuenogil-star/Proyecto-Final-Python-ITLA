"""Lectura de ajustes locales desde un archivo JSON."""
import json
from pathlib import Path


def cargar_configuracion(ruta: str | Path = None) -> dict:
    """Carga el símbolo monetario y el título de la aplicación."""
    ruta = Path(ruta) if ruta is not None else Path(__file__).with_name("configuracion.json")
    with ruta.open("r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, dict) or not isinstance(datos.get("moneda"), str):
        raise ValueError("El archivo de configuración no tiene un formato válido.")
    return datos
