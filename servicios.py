"""Reglas de negocio separadas de la pantalla y de SQLite."""
from modelos import Gasto, validar_descripcion, validar_categoria, convertir_a_centavos, validar_fecha
from base_datos import RepositorioGastos


class GestorGastos:
    """Coordina validaciones, operaciones y consultas del sistema."""

    def __init__(self, repositorio: RepositorioGastos):
        self.repositorio = repositorio

    def preparar_gasto(self, descripcion: str, categoria: str, monto: str, fecha: str,
                       identificador: int | None = None) -> Gasto:
        """Construye un gasto válido a partir de entradas del usuario."""
        return Gasto(
            descripcion=validar_descripcion(descripcion),
            categoria=validar_categoria(categoria),
            monto_centavos=convertir_a_centavos(monto),
            fecha=validar_fecha(fecha),
            id=identificador
        )

    def agregar(self, descripcion: str, categoria: str, monto: str, fecha: str) -> int:
        """Valida y guarda un gasto en la base de datos."""
        gasto = self.preparar_gasto(descripcion, categoria, monto, fecha)
        return self.repositorio.agregar(gasto)

    def actualizar(self, identificador: int, descripcion: str, categoria: str,
                   monto: str, fecha: str) -> bool:
        """Modifica un gasto existente después de validar sus datos."""
        gasto = self.preparar_gasto(descripcion, categoria, monto, fecha, identificador)
        return self.repositorio.actualizar(gasto)

    def eliminar(self, identificador: int) -> bool:
        """Borra un gasto por su identificador."""
        return self.repositorio.eliminar(identificador)

    def resumen_mensual(self, mes: str) -> dict:
        """Entrega el total, categorías y cantidad de gastos del mes."""
        filas = self.repositorio.resumen(mes)
        return {
            "mes": mes,
            "total_centavos": sum(total for _, total, _ in filas),
            "cantidad": sum(cantidad for _, _, cantidad in filas),
            "categorias": filas
        }
