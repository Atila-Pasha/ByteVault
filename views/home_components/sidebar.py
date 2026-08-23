import flet as ft

from views.home_components.theme import PURPLE, SURFACE

MENU_ITEMS = ((ft.Icons.HOME, "Home"), (ft.Icons.STAR, "Favorites"), (ft.Icons.ACCESS_TIME, "Recent"), (ft.Icons.DELETE, "Trash"), (ft.Icons.SETTINGS, "Settings"))


def build_sidebar(selected_menu: str, on_select) -> tuple[ft.Container, list[ft.Container]]:
    items = [
        ft.Container(data=label, padding=10, border=ft.Border(bottom=ft.BorderSide(3, PURPLE if label == selected_menu else "transparent")), border_radius=10, ink=True, on_click=on_select, content=ft.Row(controls=[ft.Icon(icon), ft.Text(label)]))
        for icon, label in MENU_ITEMS
    ]
    controls = items[:-1] + [ft.Container(expand=True), ft.Divider(), items[-1]]
    return ft.Container(expand=True, bgcolor=SURFACE, border_radius=10, padding=15, content=ft.Column(expand=True, controls=controls)), items
