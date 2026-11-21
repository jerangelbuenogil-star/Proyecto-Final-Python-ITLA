"""Carga diez ejemplos realistas para la demostración del proyecto."""
import sqlite3
from datetime import date
from base_datos import RepositorioGastos
from servicios import GestorGastos

EJEMPLOS = [
    ("Compra de supermercado", "Alimentación", "1850.50", "2026-11-02"),
    ("Pasaje de transporte", "Transporte", "150.00", "2026-11-03"),
    ("Materiales para clases", "Educación", "735.00", "2026-11-04"),
    ("Medicinas de farmacia", "Salud", "480.25", "2026-11-05"),
    ("Pago de internet", "Vivienda", "1200.00", "2026-11-06"),
    ("Comida de mediodía", "Alimentación", "325.00", "2026-11-07"),
    ("Recarga de transporte", "Transporte", "200.00", "2026-11-08"),
    ("Entrada al cine", "Entretenimiento", "400.00", "2026-11-09"),
    ("Fotocopias de apuntes", "Educación", "110.00", "2026-11-10"),
    ("Compra de agua", "Alimentación", "175.75", "2026-11-11"),
]


def main():
    """Inserta los registros si no existen gastos previos."""
    try:
        gestor = GestorGastos(RepositorioGastos())
        if gestor.repositorio.listar():
            print("Ya hay datos; no se insertarán duplicados.")
            return
        for descripcion, categoria, monto, fecha in EJEMPLOS:
            gestor.agregar(descripcion, categoria, monto, fecha)
        print(f"Listo: {len(EJEMPLOS)} gastos de ejemplo cargados en SQLite.")
    except (sqlite3.Error, OSError, ValueError) as error:
        print(f"Error al crear los ejemplos: {error}")


if __name__ == "__main__":
    main()
