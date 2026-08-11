import flet as ft
import json

from repositories.snippet import create_snippet_func, delete_all_snippets, get_snippets
from database.db import SessionLocal
from repositories.user import get_user, update_user
from utils.crypto import encrypt, decrypt
from views.statistics import statistics_view



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
                bgcolor=PURPLE
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
        def click_firstname(e):
            first_name_field.border_color = "transparent"
            page.update()
        
        def save_account_info(e):
            if not first_name_field.value.strip():
                first_name_field.border_color = "red"
                show_notification("Firstname can't be None")
                page.update()
                
            else:
                db = SessionLocal()
                try:
                    user_obj = get_user(db)
                    update_user(
                        db,
                        user_obj,
                        first_name_field.value,
                        last_name_field.value,
                        bio_field.value
                    )
                    show_notification("User Updated")
                    page.update()
                except Exception as e:
                    page.update()
                finally:
                    db.close()
                    
                page.update()

        
        db = SessionLocal()
        try:
            user_obj = get_user(db)
        finally:
            db.close()
            
            
        
        def confirm_delete_all(e):
            
            def close_dialog(e):
                page.pop_dialog()

            def delete_all(e):
                db = SessionLocal()

                try:
                    delete_all_snippets(db)
                    show_notification("All snippets deleted successfully.")
                    page.pop_dialog()
                    
                except Exception as error:
                    db.rollback()
                    show_notification("Failed to delete snippets.")
                finally:
                    db.close()

                page.pop_dialog()

            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Delete All Snippets?"),
                content=ft.Text(
                    "Are you sure you want to delete all your saved snippets?\n"
                    "This action cannot be undone."
                ),
                actions=[
                    ft.TextButton(
                        "No",
                        on_click=close_dialog,
                    ),
                    ft.ElevatedButton(
                        "Yes",
                        bgcolor="#EF4444",
                        color="white",
                        on_click=delete_all,
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.show_dialog(dialog)
            
        
        if selected_tab == "Account":
            title = "Account Settings"
            subtitle = "Manage your account information."

            first_name_field = ft.TextField(
                label="First Name",
                value=user_obj.firstname,
                expand=True,
                bgcolor=CARD,
                border_color="transparent",
                focused_border_color=PURPLE,
                cursor_color=PURPLE,
                text_style=ft.TextStyle(color="white"),
                hint_style=ft.TextStyle(color=TEXT_SECONDARY),
                border_radius=12,
                on_click=click_firstname
            )

            last_name_field = ft.TextField(
                label="Last Name",
                value=user_obj.lastname,
                border_radius=12,
                expand=True,
                bgcolor=CARD,
                border_color="transparent",
                focused_border_color=PURPLE,
                cursor_color=PURPLE,
                text_style=ft.TextStyle(color="white"),
                hint_style=ft.TextStyle(color=TEXT_SECONDARY),

            )

            bio_field = ft.TextField(
                label="Bio",
                value=user_obj.bio,
                multiline=True,
                min_lines=3,
                max_lines=4,
                bgcolor=CARD,
                border_color="transparent",
                focused_border_color=PURPLE,
                cursor_color=PURPLE,
                text_style=ft.TextStyle(color="white"),
                hint_style=ft.TextStyle(color=TEXT_SECONDARY),
                border_radius=12,
                expand=True
            )


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

                ft.Container(height=10),


                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.CircleAvatar(
                        radius=55,
                        bgcolor="#1D2148",
                        content=ft.Icon(
                            ft.Icons.PERSON,
                            size=55,
                            color=PURPLE,
                        ),
                    ),
                ),

                ft.Container(height=15),


                ft.Row(
                    spacing=20,
                    controls=[
                        first_name_field,
                        last_name_field,
                    ],
                ),

                bio_field,

                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.ElevatedButton(
                            "Save Changes",
                            icon=ft.Icons.SAVE,
                            bgcolor=PURPLE,
                            color="white",
                            height=42,
                            on_click=save_account_info
                        ),
                    ],
                ),

                ft.Container(height=10),


                ft.Divider(
                    color="#1E293B",
                    height=1,
                ),

                ft.Container(height=5),


                ft.Text(
                    "Danger Zone",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#EF4444",
                ),

                ft.Text(
                    "Delete all your saved snippets. This action cannot be undone.",
                    size=13,
                    color=TEXT_SECONDARY,
                ),

                ft.Container(
                    bgcolor="#1A1115",
                    border_radius=12,
                    padding=18,
                    content=ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor="#2A151B",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.DELETE_FOREVER,
                                    color="#EF4444",
                                    size=24,
                                ),
                            ),

                            ft.Column(
                                expand=True,
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        "Delete All Snippets",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        "Permanently remove all your saved snippets.",
                                        size=13,
                                        color=TEXT_SECONDARY,
                                    ),
                                ],
                            ),

                            ft.OutlinedButton(
                                "Delete All",
                                icon=ft.Icons.DELETE_FOREVER,
                                style=ft.ButtonStyle(
                                    color="#EF4444",
                                ),
                                on_click=confirm_delete_all
                            ),
                        ],
                    ),
                ),
            ]

        elif selected_tab == "Statistics":
            controls = [
                statistics_view(page)
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
            scroll=ft.ScrollMode.AUTO,
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