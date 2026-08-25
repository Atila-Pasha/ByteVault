import flet as ft


def user_avatar(user, *, radius: int | None = None) -> ft.CircleAvatar:
    """Render a user's stored photo, falling back to their initials."""
    initials = (user.firstname or "?")[:2].upper()
    return ft.CircleAvatar(
        radius=radius,
        foreground_image_src=user.profile_photo or None,
        content=ft.Text(initials),
        bgcolor="#1E293B",
        color="white",
    )
