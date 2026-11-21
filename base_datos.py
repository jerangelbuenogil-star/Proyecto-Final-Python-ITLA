"""Acceso a la base de datos SQLite para gastos personales."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from modelos import Gasto


class RepositorioGastos:
    """Guarda, consulta, modifica y elimina gastos en SQLite."""

    def __init__(self, ruta: str | Path = "datos/gastos.db"):
        self.ruta = Path(ruta)
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.crear_tabla()

    @contextmanager
    def conexion(self):
        """Abre una conexión y garantiza cierre, commit o rollback."""
        con = sqlite3.connect(self.ruta)
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def crear_tabla(self):
        """Prepara la tabla y un índice para búsquedas por fecha."""
        with self.conexion() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS gastos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    monto_centavos INTEGER NOT NULL CHECK (monto_centavos > 0),
                    fecha TEXT NOT NULL
                )
            """)
            con.execute("CREATE INDEX IF NOT EXISTS idx_gastos_fecha ON gastos(fecha)")

    @staticmethod
    def _gasto(fila):
        """Convierte una fila SQLite en un objeto Gasto."""
        return Gasto(**dict(fila)) if fila else None

    def agregar(self, gasto: Gasto) -> int:
        """Registra un gasto y devuelve su identificador."""
        with self.conexion() as con:
            cursor = con.execute(
                "INSERT INTO gastos (descripcion, categoria, monto_centavos, fecha) VALUES (?, ?, ?, ?)",
                (gasto.descripcion, gasto.categoria, gasto.monto_centavos, gasto.fecha)
            )
            return cursor.lastrowid

    def listar(self, mes: str | None = None) -> list[Gasto]:
        """Lista los gastos; opcionalmente filtra un mes AAAA-MM."""
        sql = "SELECT * FROM gastos"
        parametros = ()
        if mes is not None:
            sql += " WHERE substr(fecha, 1, 7) = ?"
            parametros = (mes,)
        sql += " ORDER BY fecha DESC, id DESC"
        with self.conexion() as con:
            return [self._gasto(fila) for fila in con.execute(sql, parametros)]

    def obtener(self, identificador: int) -> Gasto | None:
        """Busca un gasto según su identificador."""
        with self.conexion() as con:
            fila = con.execute("SELECT * FROM gastos WHERE id = ?", (identificador,)).fetchone()
        return self._gasto(fila)

    def actualizar(self, gasto: Gasto) -> bool:
        """Actualiza un gasto y señala si realmente existía."""
        with self.conexion() as con:
            cursor = con.execute("""
                UPDATE gastos SET descripcion = ?, categoria = ?, monto_centavos = ?, fecha = ?
                WHERE id = ?
            """, (gasto.descripcion, gasto.categoria, gasto.monto_centavos, gasto.fecha, gasto.id))
            return cursor.rowcount > 0

    def eliminar(self, identificador: int) -> bool:
        """Elimina el registro con el identificador solicitado."""
        with self.conexion() as con:
            cursor = con.execute("DELETE FROM gastos WHERE id = ?", (identificador,))
            return cursor.rowcount > 0

    def resumen(self, mes: str) -> list[tuple[str, int, int]]:
        """Agrupa gastos por categoría, suma importes y cuenta registros."""
        with self.conexion() as con:
            filas = con.execute("""
                SELECT categoria, SUM(monto_centavos) AS total, COUNT(*) AS cantidad
                FROM gastos WHERE substr(fecha, 1, 7) = ?
                GROUP BY categoria ORDER BY total DESC, categoria
            """, (mes,)).fetchall()
        return [(fila["categoria"], fila["total"], fila["cantidad"]) for fila in filas]
