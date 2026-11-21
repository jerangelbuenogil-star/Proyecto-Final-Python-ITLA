"""Punto de entrada del proyecto final integrador."""
import sqlite3
from base_datos import RepositorioGastos
from configuracion import cargar_configuracion
from servicios import GestorGastos
from interfaz import ejecutar


def main():
    """Inicializa los componentes y arranca la interfaz del programa."""
    try:
        datos = cargar_configuracion()
        print(datos.get("titulo", "Control de gastos personales"))
        ejecutar(GestorGastos(RepositorioGastos()))
    except (sqlite3.Error, OSError, ValueError) as error:
        print(f"No se pudo iniciar el sistema: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nSesión finalizada sin perder los gastos guardados.")


if __name__ == "__main__":
    main()
