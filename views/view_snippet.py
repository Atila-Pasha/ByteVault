import flet as ft
import flet_code_editor as fce

from database.db import SessionLocal
from repositories.snippet import get_snippet_by_id


def view_snippet_view(page: ft.Page, snippet_id: int):
    
    async def go_home(e):
        await page.push_route("/home")

    db = SessionLocal()
                
    try:
        snippet_obj = get_snippet_by_id(
            db,
            snippet_id,
        )
        
        snippet_obj.view_count = snippet_obj.view_count + 1
        db.commit()
        db.refresh(snippet_obj)
    finally:
        db.close()
        
        


    info_card = ft.Container(
        expand=True,
        bgcolor="#161D2B",
        border_radius=12,
        border=ft.Border.all(1, "#2B3342"),
        padding=20,
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    snippet_obj.title,
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                                ft.Text(
                                    snippet_obj.description or "No description",
                                    color="#98A2B3",
                                    size=14,
                                ),
                            ],
                        ),

                        ft.Icon(
                            ft.Icons.STAR,
                            color=ft.Colors.YELLOW
                            if snippet_obj.is_favorite
                            else "#667085",
                            size=28,
                        ),
                    ],
                ),

                ft.Divider(color="#263041"),

                ft.Row(
                    spacing=25,
                    controls=[
                        ft.Container(
                            width=48,
                            height=48,
                            border_radius=12,
                            border=ft.Border(
                                top=ft.BorderSide(1, "#8B5CF6"),
                                right=ft.BorderSide(1, "#8B5CF6"),
                                bottom=ft.BorderSide(1, "#8B5CF6"),
                                left=ft.BorderSide(1, "#8B5CF6"),
                            ),
                            alignment=ft.Alignment(0, 0),
                            content=ft.Image(
                                src=f"assets/languages/{snippet_obj.language}.svg",
                                width=32,
                                height=32,

                            ),
                        ),

                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.VISIBILITY,
                                    color="#98A2B3",
                                    size=18,
                                ),
                                ft.Text(
                                    str(snippet_obj.view_count),
                                    color="#98A2B3",
                                ),
                            ]
                        ),

                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.ACCESS_TIME,
                                    color="#98A2B3",
                                    size=18,
                                ),
                                ft.Text(
                                    snippet_obj.created_at.strftime("%Y-%m-%d"),
                                    color="#98A2B3",
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ) 



        
    editor = fce.CodeEditor(
        language=getattr(
            fce.CodeLanguage,
            snippet_obj.language
        ),
        read_only=True,
        code_theme=fce.CodeTheme.MONOKAI,
        value=snippet_obj.code,
        expand=True,
        autocomplete=True,
        padding=15,
        text_style=ft.TextStyle(
            font_family="JetBrains Mono",
            size=14,
            color=ft.Colors.WHITE,
        ),
        gutter_style=fce.GutterStyle(
            show_line_numbers=True,
            show_folding_handles=True,
            width=55,
            text_style=ft.TextStyle(
                font_family="JetBrains Mono",
                size=13,
                color="#7A8394",
            ),
        ),
    )


    
    return ft.View(
        route=f"/view-snippet/{snippet_id}",
        bgcolor="#080C16",
        padding=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=950,
                height=670,
                bgcolor="#0F1724",
                border_radius=22,
                border=ft.Border.all(
                    1,
                    "#1E293B",
                ),
                padding=25,
                content=ft.Column(
                    spacing=18,
                    expand=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                                    icon_color="#A7B0C3",
                                    on_click=go_home,
                                ),

                                ft.Text(
                                    "View Snippet",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),
                            ],
                        ),

                        ft.Divider(
                            color="#1F2937",
                            height=1,
                        ),
                        
                        ft.Row(
                            controls=[
                                info_card
                            ]
                        ),

                        ft.Container(
                            expand=True,
                            border_radius=12,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            border=ft.Border.all(
                                1,
                                "#2B3342",
                            ),
                            content=editor,
                        ),


                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Ready",
                                    size=12,
                                    color="#667085",
                                ),
                                ft.Text(
                                    f"{snippet_obj.language.capitalize()} • UTF-8 • LF",
                                    size=12,
                                    color="#667085",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
