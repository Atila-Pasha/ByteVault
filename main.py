import asyncio
import flet as ft

from database.db import SessionLocal, init_database
from repositories.user import create_user, get_user

from views.edit_snippet import edit_snippet_view
from views.home import home_view
from views.loading_page import loading_view
from views.view_snippet import view_snippet_view
from views.welcome import welcome_view
from views.add_snippet import new_snippet_view


async def main(page: ft.Page):
    page.title = "ByteVault"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#080C16"
    page.window.height = 700
    page.window.width = 1200

    async def handle_user_setup(
        firstname: str,
        lastname: str | None,
    ):
        db = SessionLocal()

        try:
            create_user(
                db=db,
                fname=firstname,
                lname=lastname,
            )
        finally:
            db.close()

        page.push_route("/home")

    def find_user():
        db = SessionLocal()
        try:
            return get_user(db)
        finally:
            db.close()

    async def show_startup_error():
        async def retry(e):
            await start_application()

        page.views.clear()
        page.views.append(
            loading_view(
                error="ByteVault could not finish starting. Please try again.",
                on_retry=retry,
            )
        )
        page.update()

    async def start_application():
        try:

            await asyncio.to_thread(init_database)
            user = await asyncio.to_thread(find_user)
        except Exception:
            await show_startup_error()
            return

        await page.push_route("/home" if user else "/welcome")

    async def route_change(e):
        page.views.clear()

        if page.route == "/loading":
            page.views.append(loading_view())
            page.update()

            await asyncio.sleep(0)
            await start_application()
            return

        elif page.route == "/welcome":
            page.views.append(
                welcome_view(
                    on_continue=handle_user_setup,
                )
            )

        elif page.route == "/home":
            page.views.append(home_view(page))
            
        elif page.route == "/new-snippet":
                    page.views.append(new_snippet_view(page))
        
        elif page.route.startswith("/edit-snippet/"):
            snippet_id = int(page.route.split("/")[-1])
            page.views.append(
                edit_snippet_view(
                    page,
                    snippet_id,
                )
            )
        elif page.route.startswith("/view-snippet/"):
            snippet_id = int(page.route.split("/")[-1])
            page.views.append(
                view_snippet_view(
                    page,
                    snippet_id,
                )
            )

        page.update()

    page.on_route_change = route_change
    
    await page.push_route("/loading")


ft.run(main, assets_dir="assets")

