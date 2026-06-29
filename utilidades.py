# FUNCIONES DE UTILIDAD
# Aca estan las herramientas que se reusan en todo el proyecto:
# - snackbar: muestra un mensaje temporal en pantalla
# - volver_dueno / volver_cliente: navegan entre pantallas

import flet as ft

# Muestra un mensaje en la parte inferior de la pantalla (SnackBar de Flet)
def snackbar(page, msg):
    page.snack_bar = ft.SnackBar(content=ft.Text(msg))
    page.snack_bar.open = True
    page.update()

# Vuelve al menu del dueño
# Usa import dentro de la funcion para evitar importacion circular
# (main importa de los modulos, y los modulos llaman a funciones de main)
def volver_dueno(page):
    from main import mostrar_menu_dueno
    mostrar_menu_dueno(page)

# Vuelve al panel del cliente
def volver_cliente(page):
    from main import mostrar_pantalla_cliente
    mostrar_pantalla_cliente(page)
