import flet as ft


def abrir_admin(page):

    page.clean()

    page.add(

        ft.Text(
            "PANEL ADMIN",
            size=30
        ),

        ft.ElevatedButton(
            "Agregar Pelicula"
        ),

        ft.ElevatedButton(
            "Eliminar Pelicula"
        ),

        ft.ElevatedButton(
            "Ver Usuarios"
        )

    )