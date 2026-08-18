import flet as ft

from database.db import init_database


def loading_view():
    
    init_database()

    return ft.View(
        route="/loading",
        bgcolor="#080C16",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    width=320,
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[

                        ft.Image(
                            src="logo.png",
                            width=100,
                            height=100
                        ),

                        ft.Container(height=28),

                        ft.Row(
                            spacing=0,
                            controls=[
                                ft.Text(
                                    "Byte",
                                    color=ft.Colors.WHITE,
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Vault",
                                    color="#7C5CFF",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),

                        ft.Container(height=10),

                        ft.Text(
                            "Your code. Always with you.",
                            size=15,
                            color="#8E95A5",
                        ),

                        ft.Container(height=75),

                        ft.ProgressBar(
                            value=None,
                            width=170,
                            height=4,
                            color="#7C5CFF",
                            bgcolor="#232838",
                            border_radius=10,
                        ),

                        ft.Container(height=14),

                        ft.Text(
                            "Loading your vault...",
                            size=13,
                            color="#727A8A",
                        ),
                    ],
                ),
            )
        ],
    )