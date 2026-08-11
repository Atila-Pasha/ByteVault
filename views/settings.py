import flet as ft
import json

from repositories.snippet import create_snippet_func, get_snippets
from database.db import SessionLocal
from utils.crypto import encrypt, decrypt



BG = "#0A0F1F"
SURFACE = "#0F172A"
CARD = "#111827"
TEXT_SECONDARY = "#94A3B8"
PURPLE = "#8B5CF6"


def settings_view(page: ft.Page) -> ft.Control:
    
    def show_notification(message: str):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(message),
                duration=3000,
            )
        )
        
    
    file_picker = ft.FilePicker()


    async def import_snippets(e):
        files = await file_picker.pick_files(
            dialog_title="Import ByteVault Snippets",
            allow_multiple=False,
            allowed_extensions=["bytv"],
        )

        if not files:
            return

        file = files[0]

        try:

            with open(file.path, "rb") as f:
                encrypted_data = f.read()


            decrypted_data = decrypt(encrypted_data)


            data = json.loads(
                decrypted_data.decode("utf-8")
            )

            if data.get("format") != "bytv":
                print("Invalid ByteVault file.")
                return

            snippets = data.get("snippets", [])

            db = SessionLocal()

            try:
                for snippet in snippets:
                    create_snippet_func(
                        db=db,
                        title=snippet["title"],
                        language=snippet["language"],
                        code=snippet["code"],
                        description=snippet.get("description"),
                        is_favorite=snippet.get("is_favorite", False),
                    )

            finally:
                db.close()

            print(f"Imported {len(snippets)} snippets successfully.")
            show_notification(
                f"{len(snippets)} snippets imported successfully."
            )

        except Exception as error:
            print("Import failed:", error)
        
        
        
    async def export_snippets(e):
        db = SessionLocal()

        try:
            snippets = get_snippets(db)

            data = {
                "format": "bytv",
                "version": 1,
                "snippets": [
                    {
                        "title": snippet.title,
                        "description": snippet.description,
                        "code": snippet.code,
                        "language": snippet.language,
                        "is_favorite": snippet.is_favorite,
                    }
                    for snippet in snippets
                ],
            }

            json_data = json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
            
            encrypted_data = encrypt(
                json_data.encode("utf-8")
            )

            path = await file_picker.save_file(
                dialog_title="Export ByteVault Snippets",
                file_name="bytevault_backup.bytv",
                src_bytes=encrypted_data,
            )

            if path:
                print(f"Exported {len(snippets)} snippets to: {path}")
                
                show_notification(
                    f"{len(snippets)} snippets exported successfully."
                )

        finally:
            db.close()
            
            

    selected_tab = "Account"

    content = ft.Container(
        expand=True,
    )

    tab_items = []
        

    def build_content():
        if selected_tab == "Account":
            title = "Account Settings"
            subtitle = "Manage your account information."

            controls = [
                ft.Text(
                    title,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    subtitle,
                    color=TEXT_SECONDARY,
                    size=14,
                ),
            ]

        elif selected_tab == "Statistics":
            title = "Statistics"
            subtitle = "your Statistics"

            controls = [
                ft.Text(
                    title,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    subtitle,
                    color=TEXT_SECONDARY,
                    size=14,
                ),
            ]

        else:
            title = "Import / Export"
            subtitle = "Import or export your snippets."

            controls = [
                ft.Text(
                    title,
                    size=26,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    subtitle,
                    color=TEXT_SECONDARY,
                    size=14,
                ),

                ft.Container(height=15),

                ft.Container(
                    bgcolor=SURFACE,
                    border_radius=12,
                    padding=18,
                    content=ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor="#1D2148",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.UPLOAD_FILE,
                                    color=PURPLE,
                                    size=24,
                                ),
                            ),

                            ft.Column(
                                expand=True,
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        "Export Snippets",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Export your snippets as a ByteVault file.",
                                        size=13,
                                        color=TEXT_SECONDARY,
                                    ),
                                ],
                            ),

                            ft.ElevatedButton(
                                "Export",
                                icon=ft.Icons.UPLOAD,
                                bgcolor=PURPLE,
                                color="white",
                                on_click=export_snippets
                            ),
                        ],
                    ),
                ),

                ft.Container(height=5),

                # Import
                ft.Container(
                    bgcolor=SURFACE,
                    border_radius=12,
                    padding=18,
                    content=ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor="#1D2148",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.DOWNLOAD,
                                    color=PURPLE,
                                    size=24,
                                ),
                            ),

                            ft.Column(
                                expand=True,
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        "Import Snippets",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Import snippets from a ByteVault file.",
                                        size=13,
                                        color=TEXT_SECONDARY,
                                    ),
                                ],
                            ),

                            ft.OutlinedButton(
                                "Import",
                                icon=ft.Icons.DOWNLOAD,
                                on_click=import_snippets
                            ),
                        ],
                    ),
                ),
            ]

        content.content = ft.Column(
            spacing=5,
            controls=controls,
        )

    def tab_click(e):
        nonlocal selected_tab

        selected_tab = e.control.data

        for item in tab_items:
            item.bgcolor = (
                "#1D2148"
                if item.data == selected_tab
                else "transparent"
            )

        build_content()
        page.update()

    def tab(icon, title):
        item = ft.Container(
            data=title,
            padding=10,
            border_radius=8,
            bgcolor="#1D2148" if title == selected_tab else "transparent",
            ink=True,
            on_click=tab_click,
            content=ft.Row(
                spacing=10,
                controls=[
                    ft.Icon(icon, size=18),
                    ft.Text(title),
                ],
            ),
        )

        tab_items.append(item)
        return item

    build_content()

    return ft.Column(
        expand=True,
        spacing=20,
        controls=[
            ft.Text(
                "Settings",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Row(
                expand=True,
                spacing=20,
                controls=[
                    ft.Container(
                        width=190,
                        bgcolor=SURFACE,
                        border_radius=10,
                        padding=10,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                tab(ft.Icons.PERSON, "Account"),
                                tab(ft.Icons.BAR_CHART, "Statistics"),
                                tab(ft.Icons.CODE, "Import / Export"),
                            ],
                        ),
                    ),

                    ft.Container(
                        expand=True,
                        bgcolor=CARD,
                        border_radius=12,
                        padding=25,
                        content=content,
                    ),
                ],
            ),
        ],
    )