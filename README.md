# Proyecto Final Integrador: Control de Gastos Personales

## Descripción
Aplicación de consola en Python que permite registrar, consultar, modificar y eliminar gastos personales, además de consultar resúmenes mensuales y exportar reportes CSV en pesos dominicanos (RD$).

## Problema y justificación
Cuando los gastos se apuntan en papeles o se dejan sin registrar, es difícil saber cuánto dinero se utilizó y en qué categorías. Este programa permite organizar los gastos en una sola base de datos local y obtener un resumen por mes.

## Planificación y alcance
**Problema:** una persona puede perder el control de sus gastos cuando utiliza notas sueltas o no lleva registros. Esto dificulta identificar cuánto gastó y en qué categorías. **Solución:** una aplicación local y sencilla para registrar y consultar gastos.

**Incluye:** crear, consultar, actualizar y eliminar gastos; filtros por mes; resúmenes por categoría; exportación CSV; persistencia SQLite y validación de entradas.

**No incluye:** banca en línea, transferencias, pagos reales, aplicaciones móviles, acceso por internet ni sincronización entre equipos.

### Requisitos principales
- RF-01: registrar un gasto con descripción, categoría, monto positivo y fecha válida.
- RF-02: consultar registros y filtrar por mes.
- RF-03: actualizar y eliminar registros existentes por identificador.
- RF-04: generar resumen mensual y archivo CSV.
- RNF-01: validar datos incorrectos mostrando mensajes legibles.
- RNF-02: conservar los datos después de cerrar y reabrir el programa.
- RNF-03: funcionar localmente sin enviar datos personales a internet.

## Funcionalidades
- Registrar gastos con descripción, categoría, monto y fecha.
- Consultar todos los gastos o los de un mes.
- Modificar y eliminar gastos identificados por número.
- Mostrar el total mensual agrupado por categoría.
- Exportar un mes a CSV, legible en Excel.
- Conservar datos en SQLite incluso después de salir.
- Validar entradas y mostrar mensajes claros al cometer errores.

## Tecnologías y librerías
- Python 3.10 o superior.
- SQLite (`sqlite3`, biblioteca estándar).
- CSV, JSON, `decimal`, `datetime`, `pathlib` y `unittest` (biblioteca estándar).
- `tabulate==0.9.0`, **librería externa** instalada con `pip`, para visualizar tablas en consola.

## Requisitos previos
Tener Python 3.10 o superior y conexión a internet para instalar `tabulate` la primera vez.

## Instalación en Windows
1. Descomprimir el ZIP y abrir una terminal en la carpeta del proyecto.
2. Crear el entorno virtual: `py -m venv venv`
3. Activarlo: `venv\Scripts\activate`
4. Instalar dependencias: `py -m pip install -r requirements.txt`
5. Ejecutar la aplicación: `py main.py`

**Linux o macOS:** usar `python3 -m venv venv`, `source venv/bin/activate`, `python3 -m pip install -r requirements.txt` y `python3 main.py`.

## Uso y ejemplos
El menú de opciones se presenta al iniciar:

```text
1. Registrar gasto
2. Ver todos los gastos
3. Ver gastos por mes
4. Modificar gasto
5. Eliminar gasto
6. Resumen mensual
7. Exportar gastos a CSV
0. Salir
```

Ejemplo: seleccionar **1**, escribir `Compra de supermercado`, elegir `Alimentación`, escribir `1850.50` y fecha `2026-11-02`. El sistema guardará un identificador. Para consultar el resumen del mes, seleccionar **6** y escribir `2026-11`. Para exportar el reporte, elegir **7** y escribir ese mes: se genera `reportes/gastos_2026-11.csv`.

### Preparar datos para la demostración
Ejecutar **una sola vez** `py datos_demo.py` (o `python datos_demo.py`). Inserta diez registros de ejemplo si la base de datos está vacía. La base de datos se crea automáticamente al iniciar el programa. El repositorio no publica la base de datos: para preparar los diez registros de ejemplo en tu computadora, ejecuta `py datos_demo.py` **antes de la demostración**. Para empezar con datos nuevos, elimina `datos/gastos.db` con el programa cerrado y vuelve a ejecutar `main.py`.

### Pruebas
Desde la carpeta raíz:

```bash
python -m unittest discover -s tests -v
```

Las pruebas crean bases de datos temporales independientes y comprueban altas, modificaciones, eliminaciones, validaciones, persistencia, resumen y CSV.

## Estructura de carpetas

```text
Proyecto_Final_Control_Gastos/
├── main.py                # Inicio del sistema
├── interfaz.py            # Menú y entradas del usuario
├── modelos.py             # Clase Gasto y validaciones
├── servicios.py           # Reglas del programa
├── base_datos.py          # SQLite, consultas y operaciones CRUD
├── exportacion.py         # Reportes CSV
├── configuracion.py       # Lectura de ajustes JSON
├── configuracion.json     # Configuración local
├── datos_demo.py          # Diez gastos de ejemplo
├── requirements.txt       # Librería externa
├── README.md              # Documentación del proyecto
├── .gitignore             # Archivos que no se suben a Git
├── datos/                 # Base de datos local que se crea al ejecutar
├── reportes/              # Destino de los archivos CSV
├── tests/test_sistema.py  # Pruebas automatizadas
└── documentacion/         # Informe, diagramas y evidencias
```

## Capturas de pantalla
Las siguientes evidencias corresponden a una ejecución local de la aplicación con datos de ejemplo:

**Listado de gastos**

![Listado de gastos en la consola](documentacion/captura_listado.png)

**Resumen mensual**

![Resumen mensual de gastos](documentacion/captura_resumen.png)

**Exportación a CSV**

![Confirmación de exportación CSV](documentacion/captura_exportacion.png)

Los diagramas de flujo del menú, registro y exportación están en [`documentacion/diagramas.md`](documentacion/diagramas.md).

## Diseño de los datos

| Campo | Tipo SQLite | Descripción |
| --- | --- | --- |
| id | INTEGER PRIMARY KEY | Identificador del registro |
| descripcion | TEXT | Explicación breve del gasto |
| categoria | TEXT | Grupo del gasto |
| monto_centavos | INTEGER | Cantidad positiva en centavos para evitar errores decimales |
| fecha | TEXT | Fecha ISO AAAA-MM-DD |

## Manejo de errores y seguridad
Se comprueban descripciones, montos y fechas antes de guardar. Las consultas SQL usan parámetros `?` para evitar construir sentencias SQL con texto del usuario. Las conexiones SQLite se cierran incluso si se produce un error. Se muestran mensajes si no hay registros o si el ID no existe. No se utilizan cuentas ni contraseñas.

## Repositorio GitHub
El proyecto se entrega localmente listo para publicarse. **No está publicado en GitHub todavía.** Se incluyen instrucciones sencillas en [`GUIA_PARA_SUBIR_A_GITHUB.md`](GUIA_PARA_SUBIR_A_GITHUB.md).

Si utilizas Git desde la consola (requiere tener Git instalado y autenticado):

```bash
git init
git add .
git commit -m "Proyecto final: control de gastos"
git branch -M main
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin main
```

Crear previamente un repositorio vacío en GitHub y reemplazar `URL_DE_TU_REPOSITORIO` por la URL verdadera. El `.gitignore` impide incluir bases de datos personales **cuando se utiliza Git**; si se suben archivos manualmente desde el navegador, evita seleccionar `*.db`, `.env`, `venv/`, `.venv/` y `__pycache__/`.

## Autor y datos académicos
- **Autor:** Jerangel Gabriel Bueno Gil
- **Curso:** Fundamentos de Programación
- **Carrera:** Redes de Información
- **Profesor:** Daysson Crissauris Bueno
- **Institución:** Instituto Tecnológico de las Américas (ITLA)
- **Fecha del informe:** 20 de noviembre de 2026

## Mejoras futuras
Agregar presupuestos por categoría, gráficos y búsqueda avanzada, manteniendo el sistema sencillo de usar.
