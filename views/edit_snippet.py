import flet as ft
import flet_code_editor as fce

from database.db import SessionLocal
from repositories.snippet import get_snippet_by_id
from utils.openai_api import ai_description


def edit_snippet_view(
    page: ft.Page,
    snippet_id: int
) -> ft.View:
    
    
    def api_description(e):        
        try:
            description_field.value = ai_description(editor.value)
        except:
            description_field.value = "Connection Error"
            
        page.update()


    db = SessionLocal()
                
    try:
        snippet_obj = get_snippet_by_id(
            db,
            snippet_id,
        )
    finally:
        db.close()
        
        
    def edit_snippet(e):
        if not title_field.value:
            title_field.border_color = "red"
            page.update()
            
        elif not editor.value:
            editor.value = "Please Write your Code"
            page.update()
            
        else:
            db = SessionLocal()
            
            try:
                snippet = get_snippet_by_id(
                    db,
                    snippet_id,
                )
                snippet.title = title_field.value
                snippet.description = description_field.value
                snippet.code = editor.value
                snippet.language = language_dropdown.value.upper()
                snippet.is_favorite = fov.data
                
                db.commit()
                
 
                
            finally:
                db.close()

            page.go("/home")
                
    ai_button = ft.FilledButton(
        "AI Description",
        icon=ft.Icons.GENERATING_TOKENS,
        style=ft.ButtonStyle(
            bgcolor="#8B5CF6",
            color="white",
        ),
        height=30,
        on_click=api_description
    )
                

    def title_on_click(e):
        title_field.border_color = "#2B3342"
        page.update()

    title_field = ft.TextField(
        hint_text="Enter snippet title...",
        value=snippet_obj.title,
        border_radius=10,
        height=52,
        bgcolor="#161D2B",
        border_color="#2B3342",
        focused_border_color="#7C5CFC",
        cursor_color="#7C5CFC",
        text_size=14,
        color="white",
        expand=True,
        on_click=title_on_click
    )
    
    description_field = ft.TextField(
            expand=True,
            hint_text="Enter snippet description...",
            value=snippet_obj.description,
            border_radius=10,
            height=52,
            bgcolor="#161D2B",
            border_color="#2B3342",
            focused_border_color="#7C5CFC",
            cursor_color="#7C5CFC",
            text_size=14,
            color="white",
        )
    
    
    def drop_change(e):
        tail_text.value = f"{language_dropdown.value} • UTF-8 • LF",
        editor.language = getattr(fce.CodeLanguage, e.control.value.upper())
        page.update()

        
    language_dropdown = ft.Dropdown(
        value=snippet_obj.language.capitalize(),
        bgcolor="#161D2B",
        border_color="#2B3342",
        focused_border_color="#7C5CFC",
        border_radius=10,
        color="white",
        options=[
            ft.dropdown.Option("Python"),
            ft.dropdown.Option("Java"),
            ft.dropdown.Option("JavaScript"),
            ft.dropdown.Option("Cpp"),
            ft.dropdown.Option("Go"),
            ft.dropdown.Option("Rust"),
            ft.dropdown.Option("PHP"),
            ft.dropdown.Option("SQL"),
            ft.dropdown.Option("CSS")

        ],
        on_select=drop_change
    )

    def fov_change(e):

        if e.control.data == False:
            e.control.icon = ft.Icons.STAR
            e.control.icon_color = ft.Colors.YELLOW
            e.control.data = True

        elif e.control.data == True:
            e.control.icon = ft.Icons.STAR_OUTLINE
            e.control.icon_color = ft.Colors.WHITE
            e.control.data = False

        page.update()
        
    if snippet_obj.is_favorite == True:   
        fov = ft.IconButton(
            icon=ft.Icons.STAR,
            icon_color=ft.Colors.YELLOW,
            data=True,
            on_click=fov_change
        )
    else:
        fov = ft.IconButton(
            icon=ft.Icons.STAR_OUTLINE,
            icon_color=ft.Colors.WHITE,
            data=False,
            on_click=fov_change
        )
        
    editor = fce.CodeEditor(
        language=getattr(
            fce.CodeLanguage,
            snippet_obj.language
        ),
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
    
    
    tail_text = ft.Text(
        value=f"[{snippet_obj.language.capitalize()} • UTF-8 • LF]",
        size=12,
        color="#667085",
    )

    
    return ft.View(
        route=f"/edit-snippet/{snippet_id}",
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
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[

                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="#A7B0C3",
                                    icon_size=22,
                                    on_click=lambda e: page.go("/home"),
                                ),

                                ft.Column(
                                    spacing=2,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "     Edit Snippet",
                                            size=26,
                                            weight=ft.FontWeight.BOLD,
                                            color="white",
                                        ),
                                        ft.Text(
                                            "          Update your code snippet.",
                                            size=13,
                                            color="#98A2B3",
                                        ),
                                    ],
                                ),

                                ft.Row(
                                    controls=[
                                        fov,
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK,
                                            icon_color="#7C5CFC",
                                            on_click=edit_snippet
                                        )
                                    ]
                                ),
                                
                            ],
                        ),

                        ft.Divider(
                            color="#1F2937",
                            height=1,
                        ),
                        
                        ft.Row(
                            spacing=20,
                            controls=[
                                ft.Column(
                                    expand=2,
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            "Title",
                                            size=13,
                                            color="#98A2B3",
                                        ),
                                        title_field,
                                    ],
                                ),

                                ft.Column(
                                    expand=1,
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            "Language",
                                            size=13,
                                            color="#98A2B3",
                                        ),
                                        language_dropdown,
                                    ],
                                ),
                            ],
                        ),
                        
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text(
                                    "Description",
                                    size=13,
                                    color="#98A2B3",
                                ),

                                ft.Row(
                                    spacing=12,
                                    controls=[
                                        description_field,
                                        ai_button,
                                    ],
                                ),
                            ],
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
                                tail_text,
                            ],
                        ),
                    ],
                ),
            ),
        ],
    )
