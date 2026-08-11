import flet as ft
from database.db import SessionLocal
from utils.time_ago import time_ago
from repositories.snippet import (
    get_deleted_snippets,
    get_favorite_snippets,
    get_recent_snippets,
    get_snippet_by_id,
    get_snippets,
    search_snippets,
)
from repositories.user import get_user
from utils.greeting import get_greeting
from views.settings import settings_view




BG = "#0A0F1F"
SURFACE = "#0F172A"
CARD = "#111827"
CARD_HOVER = "#1A2234"
TEXT_SECONDARY = "#94A3B8"
PURPLE = "#8B5CF6"


LANGUAGE_COLORS = {
    "PYTHON": "#3776AB",
    "JAVA": "#ED8B00",
    "JAVASCRIPT": "#F7DF1E",
    "CPP": "#00599C",
    "GO": "#00ADD8",
    "RUST": "#DEA584",
    "PHP": "#777BB4",
    "SQL": "#4479A1",
    "CSS": "#1572B6",
}



def card_hover(e):
    e.control.bgcolor = CARD_HOVER if e.data == "true" else CARD
    e.control.update()


def snippet_card(
    page,
    snippet,
    delete_snippet,
    restore_snippet,
    is_trash=False,
):
    
    language_color = LANGUAGE_COLORS.get(snippet.language, PURPLE)


    return ft.Container(
        bgcolor=CARD,
        border_radius=16,
        padding=18,
        margin=ft.Margin(0, 0, 0, 12),
        on_hover=card_hover,
        on_click=lambda e: page.go(f"/view-snippet/{snippet.id}"),
        ink=True,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[



                ft.Row(
                    spacing=16,
                    expand=True,
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
                                src=f"assets/languages/{snippet.language}.svg",
                                width=32,
                                height=32,

                            ),
                        ),

                        ft.Column(
                            expand=True,
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                            controls=[

                                ft.Text(
                                    snippet.title,
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),

                                ft.Text(
                                    snippet.description or "No description",
                                    size=13,
                                    color=TEXT_SECONDARY,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),

                                ft.Row(
                                    spacing=8,
                                    controls=[

                                        ft.Text(
                                            time_ago(snippet.updated_at),
                                            size=12,
                                            color=TEXT_SECONDARY,
                                        ),

                                        ft.Container(
                                            padding=ft.Padding(
                                                left=10,
                                                right=10,
                                                top=4,
                                                bottom=4,
                                            ),
                                            border_radius=20,
                                            content=ft.Text(
                                                snippet.language.capitalize(),
                                                size=11,
                                                weight=ft.FontWeight.W_500,
                                                color=language_color,
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),



                ft.Row(
                    spacing=8,
                    controls=[

                        ft.VerticalDivider(
                            width=20,
                            color="#25304A",
                        ),

                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            tooltip="Edit",
                            icon_color="#98A2B3",
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                bgcolor={
                                    ft.ControlState.HOVERED: "#232B45",
                                },
                            ),
                            on_click=lambda e: page.go(f"/edit-snippet/{snippet.id}"),
                        ),

                        ft.IconButton(
                            icon=(
                                ft.Icons.RESTORE_FROM_TRASH_OUTLINED
                                if is_trash
                                else ft.Icons.DELETE_OUTLINE
                            ),
                            tooltip=(
                                "Restore"
                                if is_trash
                                else "Delete"
                            ),
                            icon_color="#98A2B3",
                            style=ft.ButtonStyle(
                                shape=ft.CircleBorder(),
                                bgcolor={
                                    ft.ControlState.HOVERED:
                                        "#183222"
                                        if is_trash
                                        else "#321C1C",
                                },
                            ),
                            on_click=lambda e: restore_snippet(snippet.id) if is_trash else delete_snippet(snippet.id),
                            
                        ),
                    ],
                ),
            ],
        ),
    )



selected_menu = "Home"


    
    
def home_view(page: ft.Page) -> ft.View:
    
    
    db = SessionLocal()
    try:
        user = get_user(db)
        snippets = get_snippets(db)
    finally:
        db.close()


    def build_content(user, snippets, page):
        
        title, subtitle = get_greeting(
            
            user.firstname,
            len(snippets),
        )

        if selected_menu == "Home":

            welcome = ft.Column(
                spacing=5,
                controls=[
                    ft.Text(
                        title,
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        subtitle,
                        color=TEXT_SECONDARY,
                        size=15,
                    ),
                ],
            )

            if snippets:
                snippet_list.controls = [
                    snippet_card(
                        page,
                        snippet,
                        delete_snippet,
                        restore_snippet,
                    )
                    for snippet in snippets
                ]
            else:
                snippet_list.controls = [
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text("There are no snippets."),
                    )
                ]

            return ft.Column(
                expand=True,
                spacing=25,
                controls=[
                    welcome,

                    ft.Row(
                        controls=[
                            search_field,
                            ft.FilledButton(
                                "New Snippet",
                                icon=ft.Icons.ADD,
                                style=ft.ButtonStyle(
                                    bgcolor=PURPLE,
                                    color="white",
                                ),
                                height=42.5,
                                on_click= lambda e: page.go("/new-snippet")
                            ),
                            
                        ],
                    ),
                    
                    snippet_list,
                    
                ],
            )

        elif selected_menu == "Trash":

            welcome = ft.Column(
                spacing=5,
                controls=[
                    ft.Text(
                        "Deleted Snippets ",
                        size=34,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        f"You have {len(snippets)} deleted snippets.",
                        color=TEXT_SECONDARY,
                        size=16,
                    ),
                ],
            )

            if snippets:
                snippet_controls = [
                    snippet_card(page, snippet, delete_snippet, restore_snippet, is_trash=True)
                    for snippet in snippets
                ]
            else:
                snippet_controls = [
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text("There are no deleted snippets."),
                    )
                ]

            return ft.Column(
                expand=True,
                spacing=25,
                controls=[
                    welcome,
                    ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=snippet_controls,
                    ),
                ],
            )
            
            
        elif selected_menu == "Recent":

            welcome = ft.Column(
                spacing=5,
                controls=[
                    ft.Text(
                        "Recent Snippets",
                        size=34,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        f"Showing {len(snippets)} recently updated snippets.",
                        color=TEXT_SECONDARY,
                        size=16,
                    ),
                ],
            )

            if snippets:
                snippet_controls = [
                    snippet_card(page, snippet, delete_snippet, restore_snippet)
                    for snippet in snippets
                ]
            else:
                snippet_controls = [
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text("There are no recent snippets."),
                    )
                ]

            return ft.Column(
                expand=True,
                spacing=25,
                controls=[
                    welcome,
                    ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=snippet_controls,
                    ),
                ],
            )
            

        elif selected_menu == "Favorites":

            welcome = ft.Column(
                spacing=5,
                controls=[
                    ft.Text(
                        "Favorite Snippets",
                        size=34,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        f"You have {len(snippets)} favorite snippets.",
                        color=TEXT_SECONDARY,
                        size=16,
                    ),
                ],
            )

            if snippets:
                snippet_controls = [
                    snippet_card(page, snippet, delete_snippet, restore_snippet)
                    for snippet in snippets
                ]
            else:
                snippet_controls = [
                    ft.Container(
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text("There are no favorite snippets."),
                    )
                ]

            return ft.Column(
                expand=True,
                spacing=25,
                controls=[
                    welcome,
                    ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=snippet_controls,
                    ),
                ],
            )

        elif selected_menu == "Settings":
            return settings_view(page)
    
    




    global selected_menu


    selected_menu = "Home"
    sidebar_visible = True
    
    menu_items = []
    
    content_container = ft.Container(
        expand=True,
        padding=25,
    )
    
    snippet_list = ft.ListView(
        expand=True,
        spacing=10,
    )
    

    
    def refresh_content():

        db = SessionLocal()

        try:
            user = get_user(db)

            if selected_menu == "Favorites":
                snippets = get_favorite_snippets(db)
                
            elif selected_menu == "Trash":
                snippets = get_deleted_snippets(db)
            
            elif selected_menu == "Recent":
                snippets = get_recent_snippets(db)
                
            else:
                snippets = get_snippets(db)

        finally:
            db.close()

        content_container.content = build_content(user, snippets, page)

        page.update()
        
        
    def search_snippets_func(e):
        query = e.control.value.strip()

        db = SessionLocal()

        try:
            if query:
                snippets = search_snippets(db, query)
            else:
                snippets = get_snippets(db)
        finally:
            db.close()

        if snippets:
            snippet_list.controls = [
                snippet_card(
                    page,
                    snippet,
                    delete_snippet,
                    restore_snippet
                )
                for snippet in snippets
            ]
        else:
            snippet_list.controls = [
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text("No snippets found."),
                )
            ]

        snippet_list.update()
        
          
    def delete_snippet(snippet_id):
        db = SessionLocal()

        try:
            snippet = get_snippet_by_id(db, snippet_id)

            if snippet:
                snippet.is_deleted = True
                db.commit()

                snippets = get_snippets(db)

        finally:
            db.close()

        snippet_list.controls = [
            snippet_card(
                page,
                snippet,
                delete_snippet,
                restore_snippet
            )
            for snippet in snippets
        ]

        search_field.value = ""
        search_field.update()

        page.update()
        
    def restore_snippet(snippet_id):

        db = SessionLocal()

        try:
            snippet = get_snippet_by_id(db, snippet_id)
            snippet.is_deleted = False
            db.commit()

        finally:
            db.close()

        refresh_content()
        
    search_field = ft.TextField(
        expand=True,
        hint_text="Search snippets...",
        prefix_icon=ft.Icons.SEARCH,
        bgcolor=CARD,
        border_color="transparent",
        focused_border_color=PURPLE,
        cursor_color=PURPLE,
        text_style=ft.TextStyle(color="white"),
        hint_style=ft.TextStyle(color=TEXT_SECONDARY),
        border_radius=12,
        on_change=search_snippets_func,
    )
    
    snippet_list.controls = [
        snippet_card(
            page,
            snippet,
            delete_snippet,
            restore_snippet
        )
        for snippet in snippets
    ]
        
    sidebar_container = ft.Container(
        width=270,
        animate=ft.Animation(
            250,
            ft.AnimationCurve.EASE_IN_OUT,
        ),
    )
    
    
    
    def menu_on_click(e):
        global selected_menu

        selected_menu = e.control.data

        for item in menu_items:
            item.border = ft.Border(
                bottom=ft.BorderSide(
                    width=3,
                    color=PURPLE if item.data == selected_menu else "transparent",
                )
            )

        db = SessionLocal()

        try:
            user = get_user(db)
                            
            if selected_menu == "Favorites":
                snippets = get_favorite_snippets(db)
            elif selected_menu == "Trash":
                snippets = get_deleted_snippets(db)
            elif selected_menu == "Recent":
                snippets = get_recent_snippets(db)
            else:
                snippets = get_snippets(db)
            
        finally:
            db.close()

        content_container.content = build_content(user, snippets, e.page)

        e.page.update()
        
        
    def menu_item(icon, text, on_click, menu_items):
        item = ft.Container(
            data=text,                  
            padding=10,
            border=ft.Border(
                bottom=ft.BorderSide(
                    width=3,
                    color="#8b5CF6" if text == selected_menu else "transparent",
                )
            ),
            border_radius=10,
            ink=True,
            on_click=on_click,
            content=ft.Row(
                controls=[
                    ft.Icon(icon),
                    ft.Text(text),
                ],
            ),
        )

        menu_items.append(item)
        return item
    
    
    
    def sidebar(on_click, menu_items):

        return ft.Container(
            expand=True,
            bgcolor=SURFACE,
            border_radius=10,
            padding=15,
            content=ft.Column(
                expand=True,
                controls=[
                    

                    menu_item(ft.Icons.HOME, "Home", on_click, menu_items),
                    menu_item(ft.Icons.STAR, "Favorites", on_click, menu_items),
                    menu_item(ft.Icons.ACCESS_TIME, "Recent", on_click, menu_items),
                    menu_item(ft.Icons.DELETE, "Trash", on_click, menu_items),
                    
                    ft.Container(expand=True),
                    ft.Divider(),
                    menu_item(ft.Icons.SETTINGS, "Settings", on_click, menu_items),
                ],
            ),
        )
        
       

    def toggle_sidebar(e):
        
        nonlocal sidebar_visible
        sidebar_visible = not sidebar_visible

        sidebar_container.width = 270 if sidebar_visible else 0

        e.page.update()
    
    

    content_container.content = build_content(user, snippets, page)

    sidebar_container.content = sidebar(menu_on_click, menu_items)
    



    topbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=toggle_sidebar,
        ),
        title=ft.Row(
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
    ),
        bgcolor=SURFACE,
        actions=[
            ft.CircleAvatar(
                content=ft.Text(user.firstname[:2]),
                bgcolor="#1E293B",
                color="white",
            ),
        ],
    )

    return ft.View(
        route="/home",
        bgcolor=BG,
        appbar=topbar,
        controls=[
            ft.Row(
                expand=True,
                controls=[
                    sidebar_container,
                    content_container,
                ],
            )
        ],
    )