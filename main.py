# PUNTO DE ENTRADA DEL PROGRAMA
# Este archivo define los menus principales y conecta todos los modulos.
# La funcion main() es la que ejecuta Flet al iniciar la aplicacion.

import flet as ft
from peliculas import mostrar_registrar, mostrar_buscar, mostrar_modificar, mostrar_eliminar, mostrar_ver_peliculas
from socios import mostrar_socios
from alquileres import mostrar_alquilar, mostrar_mis_alquileres, mostrar_devolver

# Pantalla de inicio con un menu desplegable para elegir entre Dueño y Cliente
def mostrar_inicio(page):
    page.clean()
    page.add(ft.Column([ft.Text("VIDEOCLUB"), ft.PopupMenuButton(items=[ft.PopupMenuItem(content=ft.Text("Dueño"), on_click=lambda e: mostrar_menu_dueno(page)), ft.PopupMenuItem(content=ft.Text("Cliente"), on_click=lambda e: mostrar_pantalla_cliente(page))], content=ft.Text("Menu"))]))

# Menu del dueño: acceso a ABM de peliculas, socios y devoluciones
def mostrar_menu_dueno(page):
    page.clean()
    page.add(ft.Column([ft.Text("PANEL DEL DUEÑO"), ft.Text("PELICULAS"), ft.ElevatedButton("Agregar Película", on_click=lambda e: mostrar_registrar(page)), ft.ElevatedButton("Modificar Película", on_click=lambda e: mostrar_modificar(page)), ft.ElevatedButton("Eliminar Película", on_click=lambda e: mostrar_eliminar(page)), ft.ElevatedButton("Buscar Película", on_click=lambda e: mostrar_buscar(page)), ft.ElevatedButton("Socios", on_click=lambda e: mostrar_socios(page)), ft.ElevatedButton("Devolver Película", on_click=lambda e: mostrar_devolver(page)), ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inicio(page))]))

# Menu del cliente: ver catalogo, alquilar, consultar alquileres propios
def mostrar_pantalla_cliente(page):
    page.clean()
    page.add(ft.Column([ft.Text("PANEL DEL CLIENTE"), ft.ElevatedButton("Ver Películas", on_click=lambda e: mostrar_ver_peliculas(page)), ft.ElevatedButton("Alquilar", on_click=lambda e: mostrar_alquilar(page)), ft.ElevatedButton("Mis Alquileres", on_click=lambda e: mostrar_mis_alquileres(page)), ft.ElevatedButton("Volver", on_click=lambda e: mostrar_inicio(page))]))

# Configuracion inicial de la ventana de Flet
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
