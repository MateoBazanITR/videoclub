import flet as ft

def snackbar(page, msg):
    page.snack_bar = ft.SnackBar(content=ft.Text(msg))
    page.snack_bar.open = True
    page.update()

def volver_dueno(page):
    from main import mostrar_menu_dueno
    mostrar_menu_dueno(page)

def volver_cliente(page):
    from main import mostrar_pantalla_cliente
    mostrar_pantalla_cliente(page)
