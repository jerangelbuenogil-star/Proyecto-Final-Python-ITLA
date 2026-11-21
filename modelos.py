"""Modelo de datos y validaciones del sistema de gastos."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

CATEGORIAS = (
    "Alimentación", "Transporte", "Educación", "Salud",
    "Vivienda", "Entretenimiento", "Otros"
)


@dataclass
class Gasto:
    """Representa un gasto personal registrado en la aplicación."""
    descripcion: str
    categoria: str
    monto_centavos: int
    fecha: str
    id: int | None = None


def validar_descripcion(texto: str) -> str:
    """Limpia y valida una descripción de entre 3 y 100 caracteres."""
    resultado = texto.strip()
    if not 3 <= len(resultado) <= 100:
        raise ValueError("La descripción debe tener entre 3 y 100 caracteres.")
    return resultado


def validar_categoria(categoria: str) -> str:
    """Comprueba que la categoría esté incluida en las disponibles."""
    if categoria not in CATEGORIAS:
        raise ValueError("Debes seleccionar una categoría válida.")
    return categoria


def convertir_a_centavos(valor: str) -> int:
    """Convierte una cantidad positiva con hasta dos decimales en centavos."""
    try:
        cantidad = Decimal(valor.strip().replace(",", "."))
    except (InvalidOperation, AttributeError):
        raise ValueError("El monto debe ser un número válido.") from None
    if not cantidad.is_finite() or cantidad <= 0:
        raise ValueError("El monto debe ser mayor que cero.")
    if cantidad.as_tuple().exponent < -2:
        raise ValueError("El monto solo puede tener dos decimales.")
    if cantidad > Decimal("999999999.99"):
        raise ValueError("El monto excede el límite permitido.")
    return int(cantidad * 100)


def validar_fecha(texto: str) -> str:
    """Exige una fecha existente con formato AAAA-MM-DD."""
    try:
        fecha = date.fromisoformat(texto.strip())
    except (ValueError, AttributeError):
        raise ValueError("La fecha debe existir y seguir el formato AAAA-MM-DD.") from None
    if fecha.isoformat() != texto.strip():
        raise ValueError("Utiliza la fecha con formato AAAA-MM-DD.")
    return fecha.isoformat()
