"""Exportación de gastos a un archivo CSV compatible con Excel."""
import csv
from pathlib import Path
from base_datos import RepositorioGastos


def exportar_csv(repositorio: RepositorioGastos, mes: str, carpeta: str | Path = "reportes") -> Path:
    """Crea un reporte CSV del mes y devuelve la ruta guardada."""
    destino = Path(carpeta)
    destino.mkdir(parents=True, exist_ok=True)
    archivo = destino / f"gastos_{mes}.csv"
    with archivo.open("w", newline="", encoding="utf-8-sig") as f:
        escritor = csv.writer(f)
        escritor.writerow(["ID", "Descripción", "Categoría", "Monto (RD$)", "Fecha"])
        for gasto in repositorio.listar(mes):
            escritor.writerow([
                gasto.id, gasto.descripcion, gasto.categoria,
                f"{gasto.monto_centavos / 100:.2f}", gasto.fecha
            ])
    return archivo
