import flet as ft


def abrir_cliente(page):

    page.clean()

    page.add(

        ft.Text(
            "PANEL CLIENTE",
            size=30
        ),

        ft.ElevatedButton(
            "Ver Peliculas"
        ),

        ft.ElevatedButton(
            "Alquilar Pelicula"
        ),

        ft.ElevatedButton(
            "Mis Alquileres"
        )

    )