import flet as ft
from cliente import abrir_cliente
from admin import abrir_admin


def main(page: ft.Page):

    page.title = "Video Club"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 500
    page.padding = 20

    # -------------------------
    # MENU ARCHIVO
    # -------------------------

    archivo_menu = ft.PopupMenuButton(

        items=[

            ft.PopupMenuItem(
                content=ft.Text("Salir"),
                icon=ft.Icons.EXIT_TO_APP
            ),

        ],

        content=ft.Text("Archivo")

    )

    # -------------------------
    # MENU HERRAMIENTAS
    # -------------------------

    herramientas_menu = ft.PopupMenuButton(

        items=[

            ft.PopupMenuItem(

                content=ft.Row(

                    controls=[

                        ft.Image(
                            src="admin.png",
                            width=25,
                            height=25
                        ),

                        ft.Text("Admin")

                    ]

                ),

                on_click=lambda e: abrir_admin(page)

            ),

            ft.PopupMenuItem(

                content=ft.Row(

                    controls=[

                        ft.Image(
                            src="cliente.png",
                            width=25,
                            height=25
                        ),

                        ft.Text("Cliente")

                    ]

                ),

                on_click=lambda e: abrir_cliente(page)

            ),

        ],

        content=ft.Text("Herramientas")

    )

    # -------------------------
    # BOTONES
    # -------------------------

    boton1 = ft.IconButton(

        icon=ft.Icons.PERSON,
        tooltip="Cliente",
        on_click=lambda e: abrir_cliente(page)

    )

    boton2 = ft.IconButton(

        icon=ft.Icons.ADMIN_PANEL_SETTINGS,
        tooltip="Admin",
        on_click=lambda e: abrir_admin(page)

    )

    # -------------------------
    # INTERFAZ
    # -------------------------

    page.add(

        ft.Row(

            controls=[

                archivo_menu,
                herramientas_menu

            ],

            spacing=20

        ),

        ft.Container(height=20),

        ft.Row(

            controls=[

                boton1,
                boton2

            ]

        )

    )


ft.app(target=main)