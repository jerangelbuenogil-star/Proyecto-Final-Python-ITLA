"""Menús de terminal y entrada de datos. Usa tabulate (paquete externo)."""
from datetime import date
from tabulate import tabulate
from modelos import CATEGORIAS
from servicios import GestorGastos
from exportacion import exportar_csv


def seleccionar_categoria() -> str:
    """Muestra categorías y pide una opción válida."""
    print("\nCategorías disponibles:")
    for indice, categoria in enumerate(CATEGORIAS, 1):
        print(f"  {indice}. {categoria}")
    while True:
        opcion = input("Número de categoría: ").strip()
        if opcion.isdigit() and 1 <= int(opcion) <= len(CATEGORIAS):
            return CATEGORIAS[int(opcion) - 1]
        print("Elige un número de la lista.")


def pedir_identificador() -> int:
    """Solicita un identificador entero y positivo."""
    while True:
        texto = input("ID del gasto: ").strip()
        if texto.isdigit() and int(texto) > 0:
            return int(texto)
        print("El ID debe ser un número entero mayor que cero.")


def pedir_mes() -> str:
    """Solicita un mes que siga el formato AAAA-MM."""
    while True:
        mes = input(f"Mes AAAA-MM [actual: {date.today():%Y-%m}]: ").strip()
        mes = mes or date.today().strftime("%Y-%m")
        try:
            fecha = date.fromisoformat(mes + "-01")
            if fecha.strftime("%Y-%m") == mes:
                return mes
        except ValueError:
            pass
        print("Introduce un mes real con formato AAAA-MM.")


def pedir_datos(gasto=None) -> tuple[str, str, str, str]:
    """Recoge los campos para registrar o modificar un gasto."""
    if gasto is None:
        descripcion = input("Descripción: ")
        categoria = seleccionar_categoria()
        monto = input("Monto en RD$: ")
        fecha = input(f"Fecha AAAA-MM-DD [{date.today()}]: ").strip() or str(date.today())
    else:
        descripcion = input(f"Descripción [{gasto.descripcion}]: ").strip() or gasto.descripcion
        categoria = seleccionar_categoria()
        monto = input(f"Monto en RD$ [{gasto.monto_centavos / 100:.2f}]: ").strip()
        monto = monto or f"{gasto.monto_centavos / 100:.2f}"
        fecha = input(f"Fecha [{gasto.fecha}]: ").strip() or gasto.fecha
    return descripcion, categoria, monto, fecha


def mostrar_gastos(gastos):
    """Muestra la lista en una tabla fácil de leer."""
    if not gastos:
        print("No hay gastos registrados para mostrar.")
        return
    filas = [
        [g.id, g.descripcion, g.categoria, f"RD$ {g.monto_centavos / 100:,.2f}", g.fecha]
        for g in gastos
    ]
    print(tabulate(filas, headers=["ID", "Descripción", "Categoría", "Monto", "Fecha"], tablefmt="grid"))


def registrar(gestor: GestorGastos):
    """Registra un gasto después de pedir sus datos."""
    descripcion, categoria, monto, fecha = pedir_datos()
    identificador = gestor.agregar(descripcion, categoria, monto, fecha)
    print(f"Gasto registrado correctamente con ID {identificador}.")


def modificar(gestor: GestorGastos):
    """Permite editar un registro identificado por ID."""
    identificador = pedir_identificador()
    anterior = gestor.repositorio.obtener(identificador)
    if anterior is None:
        print("No se encontró un gasto con ese ID.")
        return
    descripcion, categoria, monto, fecha = pedir_datos(anterior)
    gestor.actualizar(identificador, descripcion, categoria, monto, fecha)
    print("Gasto actualizado correctamente.")


def borrar(gestor: GestorGastos):
    """Solicita una confirmación antes de eliminar."""
    identificador = pedir_identificador()
    gasto = gestor.repositorio.obtener(identificador)
    if gasto is None:
        print("No se encontró un gasto con ese ID.")
        return
    print(f"Gasto: {gasto.descripcion} - RD$ {gasto.monto_centavos / 100:.2f}")
    if input("¿Eliminar? Escribe SI para confirmar: ").strip().upper() == "SI":
        gestor.eliminar(identificador)
        print("Gasto eliminado correctamente.")
    else:
        print("Operación cancelada.")


def resumen(gestor: GestorGastos):
    """Presenta los totales y categorías de un mes."""
    datos = gestor.resumen_mensual(pedir_mes())
    if datos["cantidad"] == 0:
        print("No hay gastos en el mes indicado.")
        return
    filas = [[categoria, cantidad, f"RD$ {total / 100:,.2f}"]
             for categoria, total, cantidad in datos["categorias"]]
    print(tabulate(filas, headers=["Categoría", "Registros", "Total"], tablefmt="grid"))
    print(f"Total: RD$ {datos['total_centavos'] / 100:,.2f} ({datos['cantidad']} gastos)")


def mostrar_menu():
    """Imprime las opciones de trabajo disponibles."""
    print("\n=== CONTROL DE GASTOS PERSONALES ===")
    print("1. Registrar gasto")
    print("2. Ver todos los gastos")
    print("3. Ver gastos por mes")
    print("4. Modificar gasto")
    print("5. Eliminar gasto")
    print("6. Resumen mensual")
    print("7. Exportar gastos a CSV")
    print("0. Salir")


def ejecutar(gestor: GestorGastos):
    """Mantiene el menú activo y controla errores del usuario."""
    acciones = {"1": lambda: registrar(gestor), "2": lambda: mostrar_gastos(gestor.repositorio.listar()),
                "3": lambda: mostrar_gastos(gestor.repositorio.listar(pedir_mes())),
                "4": lambda: modificar(gestor), "5": lambda: borrar(gestor),
                "6": lambda: resumen(gestor),
                "7": lambda: print(f"Reporte creado: {exportar_csv(gestor.repositorio, pedir_mes())}")}
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()
        if opcion == "0":
            print("Hasta luego. Los datos permanecen guardados.")
            return
        try:
            if opcion in acciones:
                acciones[opcion]()
            else:
                print("Opción no válida; intenta nuevamente.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}")
