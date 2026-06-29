import flet as ft
from peliculas import mostrar_registrar, mostrar_buscar, mostrar_modificar, mostrar_eliminar, mostrar_ver_peliculas
from socios import mostrar_socios
from alquileres import mostrar_alquilar, mostrar_mis_alquileres, mostrar_devolver

def _pedir_contrasena(page):
    page.clean()
    t_pass = ft.TextField(label="Contraseña", password=True)
    def _verificar(e):
        if t_pass.value == "2020":
            mostrar_menu_dueno(page)
        else:
            from utilidades import snackbar
            snackbar(page, "Contraseña incorrecta")
    page.add(ft.Column([
        ft.Text("ACCESO DUEÑO", size=20, weight=ft.FontWeight.BOLD),
        t_pass,
        ft.ElevatedButton("Ingresar", on_click=_verificar),
        ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inicio(page)),
    ]))

def mostrar_inicio(page):
    page.clean()
    menu_ingresar = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Dueño"), icon=ft.Icons.ADMIN_PANEL_SETTINGS, on_click=lambda e: _pedir_contrasena(page)),
            ft.PopupMenuItem(content=ft.Text("Cliente"), icon=ft.Icons.PERSON, on_click=lambda e: mostrar_pantalla_cliente(page)),
        ],
        content=ft.Text("Ingresar")
    )
    page.add(ft.Column([
        ft.Text("VIDEOCLUB", size=30, weight=ft.FontWeight.BOLD),
        ft.Row([menu_ingresar]),
    ]))

def mostrar_menu_dueno(page):
    page.clean()
    peliculas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Agregar"), icon=ft.Icons.ADD, on_click=lambda e: mostrar_registrar(page)),
            ft.PopupMenuItem(content=ft.Text("Modificar"), icon=ft.Icons.EDIT, on_click=lambda e: mostrar_modificar(page)),
            ft.PopupMenuItem(content=ft.Text("Eliminar"), icon=ft.Icons.DELETE, on_click=lambda e: mostrar_eliminar(page)),
            ft.PopupMenuItem(content=ft.Text("Buscar"), icon=ft.Icons.SEARCH, on_click=lambda e: mostrar_buscar(page)),
        ],
        content=ft.Text("Películas")
    )
    socios_btn = ft.IconButton(icon=ft.Icons.GROUP, tooltip="Socios", on_click=lambda e: mostrar_socios(page))
    devolver_btn = ft.IconButton(icon=ft.Icons.ASSIGNMENT_RETURN, tooltip="Devolver", on_click=lambda e: mostrar_devolver(page))
    page.add(ft.Column([
        ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Volver", on_click=lambda e: mostrar_inicio(page)), ft.Text("PANEL DEL DUEÑO", size=20, weight=ft.FontWeight.BOLD)]),
        ft.Divider(),
        ft.Row([peliculas_menu, socios_btn, devolver_btn]),
    ]))

def mostrar_pantalla_cliente(page):
    page.clean()
    ver_btn = ft.IconButton(icon=ft.Icons.MOVIE, tooltip="Ver Películas", on_click=lambda e: mostrar_ver_peliculas(page))
    alquilar_btn = ft.IconButton(icon=ft.Icons.SHOPPING_CART, tooltip="Alquilar", on_click=lambda e: mostrar_alquilar(page))
    mis_alq_btn = ft.IconButton(icon=ft.Icons.LIST_ALT, tooltip="Mis Alquileres", on_click=lambda e: mostrar_mis_alquileres(page))
    page.add(ft.Column([
        ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK, tooltip="Volver", on_click=lambda e: mostrar_inicio(page)), ft.Text("PANEL DEL CLIENTE", size=20, weight=ft.FontWeight.BOLD)]),
        ft.Divider(),
        ft.Row([ver_btn, alquilar_btn, mis_alq_btn]),
    ]))

def main(page: ft.Page):
    page.title = "Videoclub"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 600
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO
    mostrar_inicio(page)

if __name__ == "__main__":
    ft.app(target=main)
