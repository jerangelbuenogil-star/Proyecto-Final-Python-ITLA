# Guía rápida: entregar el proyecto en GitHub

**Nombre sugerido del repositorio:** `Proyecto-Final-Control-de-Gastos`

## Parte A: probar en Windows
1. Descarga y descomprime el ZIP. Abre la carpeta que contiene `main.py`.
2. Abre la carpeta en Visual Studio Code o abre una terminal de Windows en esa ubicación.
3. Ejecuta `py -m pip install -r requirements.txt`.
4. Ejecuta `py datos_demo.py` para generar los diez gastos de ejemplo.
5. Ejecuta `py main.py` y comprueba las opciones 2 (listado), 6 (resumen) y 7 (exportación).
6. Ejecuta `py -m unittest discover -s tests -v` para comprobar las 10 pruebas.

## Parte B: publicar con el navegador
1. Accede a https://github.com/ e inicia sesión o crea una cuenta.
2. Haz clic en **New repository** (Nuevo repositorio).
3. Escribe `Proyecto-Final-Control-de-Gastos`; elige la visibilidad según lo que pida el profesor.
4. No agregues README, .gitignore ni licencia desde GitHub, porque ya están en los archivos.
5. Crea el repositorio.
6. En la pantalla del repositorio busca **uploading an existing file**, o abre **Add file → Upload files**.
7. Abre la carpeta descomprimida en tu equipo y selecciona **su contenido**, no el archivo ZIP. Arrastra archivos y subcarpetas a GitHub para mantener `README.md` y `main.py` en la raíz.
8. Verifica que los directorios `tests/` y `documentacion/` aparezcan en GitHub.
9. En el campo de confirmación escribe `Proyecto final de Fundamentos de Programación` y confirma la subida.
10. Abre el repositorio y comprueba que se muestra el README. Copia la URL del repositorio para entregar al profesor si la plataforma la solicita.

**Importante:** nunca subas una base de datos propia de gastos (`datos/gastos.db`), archivos `.env`, contraseñas, entornos virtuales o carpetas `__pycache__`. Esta entrega no incluye esos datos privados.

## Si GitHub no permite arrastrar las carpetas
Puedes subir los archivos desde GitHub Desktop o utilizar los comandos Git que están explicados en README.md. Para GitHub Desktop: crea el repositorio local desde la carpeta de este proyecto, haz commit y elige **Publish repository**. Se puede consultar la ayuda oficial de GitHub.

## Parte C: cómo demostrarlo al profesor
- Muestra la lista con diez gastos de ejemplo.
- Registra un gasto nuevo, modifica otro y elimina uno.
- Escribe un monto incorrecto para enseñar la validación de errores.
- Muestra un resumen mensual y exporta un CSV.
- Explica que SQLite guarda los datos, `interfaz.py` controla el menú, `servicios.py` aplica reglas, y `README.md` documenta la instalación.
- Ten a mano el informe y las capturas de `documentacion/`.

**Profesor:** Daysson Crissauris Bueno.
**Curso:** Fundamentos de Programación, ITLA.
