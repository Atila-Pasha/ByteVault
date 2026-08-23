import flet as ft

from utils.time_ago import time_ago
from views.home_components.theme import CARD, CARD_HOVER, LANGUAGE_COLORS, PURPLE, TEXT_SECONDARY


def _on_hover(event: ft.ControlEvent) -> None:
    event.control.bgcolor = CARD_HOVER if event.data == "true" else CARD
    event.control.update()


def snippet_card(page: ft.Page, snippet, on_delete, on_restore, *, is_trash: bool = False) -> ft.Container:
    """Build one snippet row; persistence is owned by the home controller."""
    async def go_to_edit(event: ft.ControlEvent) -> None:
        await page.push_route(f"/edit-snippet/{snippet.id}")

    async def go_to_details(event: ft.ControlEvent) -> None:
        await page.push_route(f"/view-snippet/{snippet.id}")

    language_color = LANGUAGE_COLORS.get(snippet.language, PURPLE)
    action = on_restore if is_trash else on_delete
    return ft.Container(
        bgcolor=CARD, border_radius=16, padding=18, margin=ft.Margin(0, 0, 0, 12),
        on_hover=_on_hover, on_click=go_to_details, ink=True,
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER, controls=[
            ft.Row(spacing=16, expand=True, controls=[
                ft.Container(width=48, height=48, border_radius=12, border=ft.Border.all(1, language_color), alignment=ft.Alignment(0, 0), content=ft.Image(src=f"languages/{snippet.language}.svg", width=32, height=32)),
                ft.Column(expand=True, spacing=5, horizontal_alignment=ft.CrossAxisAlignment.START, controls=[
                    ft.Text(snippet.title, size=18, weight=ft.FontWeight.BOLD, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Text(snippet.description or "No description", size=13, color=TEXT_SECONDARY, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ft.Row(spacing=8, controls=[
                        ft.Text(time_ago(snippet.updated_at), size=12, color=TEXT_SECONDARY),
                        ft.Container(padding=ft.Padding(left=10, right=10, top=4, bottom=4), border_radius=20, content=ft.Text(snippet.language.capitalize(), size=11, weight=ft.FontWeight.W_500, color=language_color)),
                    ]),
                ]),
            ]),
            ft.Row(spacing=8, controls=[
                ft.VerticalDivider(width=20, color="#25304A"),
                ft.IconButton(icon=ft.Icons.EDIT_OUTLINED, tooltip="Edit", icon_color="#98A2B3", style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor={ft.ControlState.HOVERED: "#232B45"}), on_click=go_to_edit),
                ft.IconButton(icon=ft.Icons.RESTORE_FROM_TRASH_OUTLINED if is_trash else ft.Icons.DELETE_OUTLINE, tooltip="Restore" if is_trash else "Delete", icon_color="#98A2B3", style=ft.ButtonStyle(shape=ft.CircleBorder(), bgcolor={ft.ControlState.HOVERED: "#183222" if is_trash else "#321C1C"}), on_click=lambda event: action(snippet.id)),
            ]),
        ]),
    )
