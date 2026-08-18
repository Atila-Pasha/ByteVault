from collections.abc import Callable


import flet as ft


def welcome_view(
    on_continue: Callable[[str, str | None], None],
) -> ft.View:
    firstname_field = ft.TextField(
        label="First name",
        hint_text="e.g. Name",
        width=360,
        height=58,
        border_radius=10,
        border_color="#2B3342",
        focused_border_color="#7C5CFC",
        cursor_color="#7C5CFC",
        text_size=14,
        label_style=ft.TextStyle(
            color="#8D96A8",
        ),
    )

    lastname_field = ft.TextField(
        label="Last name",
        hint_text="Optional",
        width=360,
        height=58,
        border_radius=10,
        border_color="#2B3342",
        focused_border_color="#7C5CFC",
        cursor_color="#7C5CFC",
        text_size=14,
        label_style=ft.TextStyle(
            color="#8D96A8",
        ),
    )

    error_text = ft.Text(
        "",
        color="#FF6B81",
        size=12,
        visible=False,
    )

    def handle_continue(e):
        firstname = firstname_field.value.strip()
        lastname = lastname_field.value.strip() or None

        if not firstname:
            error_text.value = "Please enter your first name."
            error_text.visible = True
            error_text.update()
            return

        on_continue(firstname, lastname)

    return ft.View(
        route="/welcome",
        bgcolor="#080C16",
        padding=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=500,
                padding=40,
                border=ft.Border.all(
                    width=1,
                    color="#1C2432",
                ),
                border_radius=18,
                bgcolor="#0D131F",
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    controls=[
                        ft.Container(
                            width=180,
                            height=160,
                           
                            alignment=ft.Alignment.CENTER,
                            content=ft.Image(
                                src="logo.png",
                                width=1000,
                                height=1000
                            ),
                        ),

                        ft.Container(height=28),

                        ft.Text(
                            "WELCOME",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#F4F6FA",
                            style=ft.TextStyle(
                                letter_spacing=2,
                            ),
                        ),

                        ft.Container(height=8),

                        ft.Text(
                            "Let's personalize your code vault.",
                            size=14,
                            color="#8993A6",
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Container(height=36),

                        ft.Column(
                            spacing=16,
                            controls=[
                                firstname_field,
                                lastname_field,
                            ],
                        ),

                        ft.Container(height=8),

                        error_text,

                        ft.Container(height=16),

                        ft.FilledButton(
                            content=ft.Text(
                                "Continue",
                                size=14,
                                weight=ft.FontWeight.W_500,
                            ),
                            width=360,
                            height=48,
                            on_click=handle_continue,
                            style=ft.ButtonStyle(
                                bgcolor="#6D4AFF",
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(
                                    radius=10,
                                ),
                            ),
                        ),

                        ft.Container(height=24),

                        ft.Text(
                            "Your code. Always with you.",
                            size=12,
                            color="#596274",
                        ),
                    ],
                ),
            ),
        ],
    )