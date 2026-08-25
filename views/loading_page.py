import flet as ft


def loading_view(
    message: str = "Loading your vault...",
    error: str | None = None,
    on_retry=None,
) -> ft.View:


    is_error = error is not None

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
                            color="#FF6B81" if is_error else "#7C5CFF",
                            bgcolor="#232838",
                            border_radius=10,
                            visible=not is_error,
                        ),

                        ft.Container(height=14),

                        ft.Text(
                            error or message,
                            size=13,
                            color="#FF6B81" if is_error else "#727A8A",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(height=14, visible=is_error),
                        ft.OutlinedButton(
                            "Try again",
                            on_click=on_retry,
                            visible=is_error,
                            style=ft.ButtonStyle(
                                color="#C7B9FF",
                                side=ft.BorderSide(1, "#7C5CFF"),
                            ),
                        ),
                    ],
                ),
            )
        ],
    )
