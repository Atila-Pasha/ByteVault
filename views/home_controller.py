"""State and orchestration for the home screen.

UI-only controls live in :mod:`views.home_components`; this class owns navigation,
database work, and the small amount of screen state.
"""

import flet as ft

from database.db import SessionLocal
from repositories.snippet import (
    empty_trash,
    get_deleted_snippets,
    get_favorite_snippets,
    get_recent_snippets,
    get_snippet_by_id,
    get_snippets,
    search_snippets,
)
from repositories.user import get_user
from utils.greeting import get_greeting
from views.home_components.sidebar import build_sidebar
from views.home_components.snippet_card import snippet_card
from views.home_components.theme import BG, CARD, PURPLE, SURFACE, TEXT_SECONDARY
from views.settings import settings_view


class HomeController:
    def __init__(self, page: ft.Page):
        self.page = page
        self.selected_menu = "Home"
        self.sidebar_visible = True
        self.menu_items: list[ft.Container] = []
        self.content = ft.Container(expand=True, padding=25)
        self.sidebar = ft.Container(width=270, animate=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT))
        self.snippet_list = ft.ListView(expand=True, spacing=10)
        self.search_field = ft.TextField(
            expand=True, hint_text="Search snippets...", prefix_icon=ft.Icons.SEARCH,
            bgcolor=CARD, border_color="transparent", focused_border_color=PURPLE,
            cursor_color=PURPLE, text_style=ft.TextStyle(color="white"),
            hint_style=ft.TextStyle(color=TEXT_SECONDARY), border_radius=12,
            on_change=self.search,
        )

    def load_data(self):
        """Fetch data for the currently selected menu and always close the session."""
        db = SessionLocal()
        try:
            user = get_user(db)
            queries = {
                "Favorites": get_favorite_snippets,
                "Trash": get_deleted_snippets,
                "Recent": get_recent_snippets,
            }
            return user, queries.get(self.selected_menu, get_snippets)(db)
        finally:
            db.close()

    async def new_snippet(self, event: ft.ControlEvent) -> None:
        await self.page.push_route("/new-snippet")

    def cards(self, snippets, *, is_trash: bool = False):
        if snippets:
            return [snippet_card(self.page, snippet, self.delete_snippet, self.restore_snippet, is_trash=is_trash) for snippet in snippets]
        message = "There are no deleted snippets." if is_trash else "There are no snippets."
        return [ft.Container(expand=True, alignment=ft.Alignment(0, 0), content=ft.Text(message))]

    def build_home_content(self, user, snippets) -> ft.Column:
        title, subtitle = get_greeting(user.firstname, len(snippets))
        self.snippet_list.controls = self.cards(snippets)
        return ft.Column(expand=True, spacing=25, controls=[
            ft.Column(spacing=5, controls=[ft.Text(title, size=30, weight=ft.FontWeight.BOLD), ft.Text(subtitle, color=TEXT_SECONDARY, size=15)]),
            ft.Row(controls=[self.search_field, ft.FilledButton("New Snippet", icon=ft.Icons.ADD, style=ft.ButtonStyle(bgcolor=PURPLE, color="white"), height=42.5, on_click=self.new_snippet)]),
            self.snippet_list,
        ])

    def build_collection_content(self, snippets, title: str, subtitle: str, *, is_trash: bool = False) -> ft.Column:
        header_controls = [ft.Text(title, size=34, weight=ft.FontWeight.BOLD)]
        if is_trash:
            header_controls.append(ft.Row(controls=[
                ft.Text(subtitle, color=TEXT_SECONDARY, size=16, expand=True),
                ft.TextButton(content=ft.Text("Empty Trash", color="red"), icon=ft.Icons.DELETE_FOREVER, icon_color="red", on_click=self.show_empty_trash_dialog),
            ]))
        else:
            header_controls.append(ft.Text(subtitle, color=TEXT_SECONDARY, size=16))
        return ft.Column(expand=True, spacing=25, controls=[
            ft.Column(spacing=5, controls=header_controls),
            ft.ListView(expand=True, spacing=10, controls=self.cards(snippets, is_trash=is_trash)),
        ])

    def build_content(self, user, snippets) -> ft.Control:
        if self.selected_menu == "Home":
            return self.build_home_content(user, snippets)
        if self.selected_menu == "Favorites":
            return self.build_collection_content(snippets, "Favorite Snippets", f"You have {len(snippets)} favorite snippets.")
        if self.selected_menu == "Recent":
            return self.build_collection_content(snippets, "Recent Snippets", f"Showing {len(snippets)} recently updated snippets.")
        if self.selected_menu == "Trash":
            return self.build_collection_content(snippets, "Deleted Snippets", f"You have {len(snippets)} deleted snippets.", is_trash=True)
        return settings_view(self.page)

    def refresh(self) -> None:
        user, snippets = self.load_data()
        self.content.content = self.build_content(user, snippets)
        self.page.update()

    def search(self, event: ft.ControlEvent) -> None:
        query = event.control.value.strip()
        db = SessionLocal()
        try:
            snippets = search_snippets(db, query) if query else get_snippets(db)
        finally:
            db.close()
        self.snippet_list.controls = self.cards(snippets) if snippets else [ft.Container(alignment=ft.Alignment(0, 0), content=ft.Text("No snippets found."))]
        self.snippet_list.update()

    def delete_snippet(self, snippet_id: int) -> None:
        db = SessionLocal()
        try:
            snippet = get_snippet_by_id(db, snippet_id)
            if snippet:
                snippet.is_deleted = True
                db.commit()
        finally:
            db.close()
        self.search_field.value = ""
        self.refresh()

    def restore_snippet(self, snippet_id: int) -> None:
        db = SessionLocal()
        try:
            snippet = get_snippet_by_id(db, snippet_id)
            if snippet:
                snippet.is_deleted = False
                db.commit()
        finally:
            db.close()
        self.refresh()

    def empty_trash(self) -> None:
        db = SessionLocal()
        try:
            empty_trash(db)
        finally:
            db.close()
        self.refresh()

    def show_empty_trash_dialog(self, event: ft.ControlEvent) -> None:
        def close_dialog(dialog_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.page.update()

        def confirm(dialog_event: ft.ControlEvent) -> None:
            dialog.open = False
            self.empty_trash()

        dialog = ft.AlertDialog(
            modal=True, title=ft.Text("Empty Trash"),
            content=ft.Text("Are you sure you want to permanently delete all deleted snippets?\nThis action cannot be undone."),
            actions=[ft.TextButton(ft.Text("Cancel", color="green"), on_click=close_dialog), ft.TextButton(ft.Text("Empty Trash", color="red"), on_click=confirm)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def select_menu(self, event: ft.ControlEvent) -> None:
        self.selected_menu = event.control.data
        for item in self.menu_items:
            item.border = ft.Border(bottom=ft.BorderSide(3, PURPLE if item.data == self.selected_menu else "transparent"))
        self.refresh()

    def toggle_sidebar(self, event: ft.ControlEvent) -> None:
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar.width = 270 if self.sidebar_visible else 0
        self.page.update()

    def view(self) -> ft.View:
        user, snippets = self.load_data()
        self.content.content = self.build_content(user, snippets)
        sidebar_content, self.menu_items = build_sidebar(self.selected_menu, self.select_menu)
        self.sidebar.content = sidebar_content
        topbar = ft.AppBar(
            leading=ft.IconButton(icon=ft.Icons.MENU, on_click=self.toggle_sidebar),
            title=ft.Row(spacing=0, controls=[ft.Text("Byte", color=ft.Colors.WHITE, size=22, weight=ft.FontWeight.BOLD), ft.Text("Vault", color="#7C5CFF", size=22, weight=ft.FontWeight.BOLD)]),
            bgcolor=SURFACE,
            actions=[ft.CircleAvatar(content=ft.Text(user.firstname[:2]), bgcolor="#1E293B", color="white")],
        )
        return ft.View(route="/home", bgcolor=BG, appbar=topbar, controls=[ft.Row(expand=True, controls=[self.sidebar, self.content])])


def home_view(page: ft.Page) -> ft.View:
    return HomeController(page).view()
