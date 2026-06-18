'''
Crea una ventana con un botón que, al hacer clic, 
muestra un menú emergente con opciones. Cada opción, al seleccionarse, 
muestra un mensaje en la consola.
'''
import flet as ft

def main(page: ft.Page):
    page.title = "Barra de Menú"

    archivo_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Copiar"), icon=ft.Icons.COPY),
            ft.PopupMenuItem(content=ft.Text("Salir"), icon=ft.Icons.EXIT_TO_APP),
        ],
        content=ft.Text("Archivo")
    )

    herramientas_menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(content=ft.Text("Cliente"), icon=ft.Icons.PERSON),
            ft.PopupMenuItem(content=ft.Text("Proveedor"), icon=ft.Icons.PERSONAL_INJURY_ROUNDED),
            ft.PopupMenuItem(content=ft.Text("Producto"), icon=ft.Icons.STORE),
            ft.PopupMenuItem(content=ft.Text("Empleado"), icon=ft.Icons.PERM_CAMERA_MIC_SHARP),
            ft.PopupMenuItem(content=ft.Text("Usuario"), icon=ft.Icons.PERSON_ADD_ALT),
        ],
        content=ft.Text("Herramientas")
    )

    boton1 = ft.IconButton(icon=ft.Icons.PERSON, tooltip="Cliente")
    boton2 = ft.IconButton(icon=ft.Icons.STORE, tooltip="Producto")
    boton3 = ft.IconButton(icon=ft.Icons.FOLDER_OPEN, tooltip="Ficha Técnica")

    page.add(
        ft.Row(
            controls=[
                archivo_menu,
                herramientas_menu
            ],
            spacing=10,
        ),
        ft.Row(
            controls=[
                boton1,
                boton2,
                boton3
            ]
        )
    )

ft.app(target=main)
#ft.app(main, view=ft.AppView.WEB_BROWSER)