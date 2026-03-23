import sys
import flet as ft
import pyautogui
from core.constants import IconCustom,Messages

class Header(ft.Container):
    def __init__(self, page : ft.Page,title: str = "None",screen_id: int = 0) -> None:
        super().__init__()
        self.page : ft.Page = page
        self.title : str = title
        self.screen_id : int = screen_id

    def build(self) -> ft.AppBar:
        appbar = ft.AppBar(
                leading_width=1400,
                elevation=0,
                bgcolor="transparent",
                elevation_on_scroll=0,
                automatically_imply_leading=True,
                leading=self._build_default_leading(),
                actions=[
                    self._build_button_toggle_desktop(),
                    self._build_button_lock_workstation(),
                    self._build_button_about(),
                    self._build_button_minimize(),
                    self._build_button_close(),
                ],
            )
        appbar.leading = self._build_header_with_menu()
        return appbar

    def _build_default_leading(self) -> ft.WindowDragArea:
        return ft.WindowDragArea(
            maximizable=False,
            content=ft.Row(
                [
                    ft.Text(""),
                ]
            )
        )

    def _build_header_with_menu(self) -> ft.WindowDragArea:
        return ft.WindowDragArea(
            maximizable=False,
            content=ft.Row(
                [
                    self._build_button_menu(),
                    ft.Text(
                        self.title,
                        size=20,
                        color=ft.Colors.WHITE,
                    ),
                ]
            )
        )

    def _build_button_menu(self) -> ft.IconButton:
        def change_screen(e: ft.ControlEvent) -> None:
            index = e.control.selected_index
            route_map = {
                0: "/",
                1: "/enviroments",
            }
            if index in route_map:
                self.page.go(route_map[index])
            self.page.update()

        def menu(e:ft.ControlEvent) -> None:
            try:
                if self.page.views[-1].drawer is None:
                   pyautogui.click()
                pantallas : list = [
                    ft.NavigationDrawerDestination(
                        label=Messages.MSG_START,
                        icon_content=ft.Image(src=IconCustom.ICON_HOUSE_DOOR, width=25, height=25,color=ft.Colors.WHITE),
                        selected_icon_content=ft.Image(src=IconCustom.ICON_HOUSE_DOOR, width=25, height=25,color=ft.Colors.WHITE),
                    ),
                    ft.NavigationDrawerDestination(
                        label=Messages.MSG_ENVIRONMENTS,
                        icon_content=ft.Image(src=IconCustom.ICON_SERVER, width=25, height=25,color=ft.Colors.WHITE),
                        selected_icon_content=ft.Image(src=IconCustom.ICON_SERVER, width=25, height=25,color=ft.Colors.WHITE),
                    ),
                ]
                drawer = ft.NavigationDrawer(
                    tile_padding=ft.padding.only(left=-1, right=4, top=4),
                    selected_index=self.screen_id,
                    on_change=lambda e: change_screen(e),
                    indicator_color=ft.Colors.BLACK45,
                    indicator_shape=ft.RoundedRectangleBorder(radius=10),
                )
                drawer.controls = pantallas
                self.page.views[-1].drawer = drawer
                self.page.open(drawer)
                self.page.update()
            except:
                pass

        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_MENU, width=25, height=25, color=ft.Colors.WHITE),
                selected=True,
                on_click=menu,
                tooltip=Messages.MSG_MENU,
           )
    
    def _build_button_toggle_desktop(self) -> ft.IconButton:
        def toggle_desktop(e:ft.ControlEvent) -> None:
            import ctypes
            shell = ctypes.WinDLL("shell32", use_last_error=True)
            try:
                shell.ShellExecuteW(None, "open", "cmd.exe", "/c powershell -NoProfile -Command \"(new-object -com shell.application).ToggleDesktop()\"", None, 0)
            except Exception as e:
                raise OSError(f"ToggleDesktop falló: {e}")

        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_TOGGLE_DESKTOP, width=25, height=25, color=ft.Colors.WHITE),
                on_click=toggle_desktop,
                tooltip="Ocultar escritorio"
            )

    def _build_button_lock_workstation(self) -> ft.IconButton:
        def lock(e:ft.ControlEvent) -> None:
            import ctypes
            ok = ctypes.windll.user32.LockWorkStation()
            if not ok:
                raise OSError("LockWorkStation failed")
        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_LOCK_WORKSTATION, width=23, height=23, color=ft.Colors.WHITE),
                on_click=lock,
                tooltip="Bloquear estación de trabajo"
            )

    def _build_button_about(self) -> ft.IconButton:
        def about(e : ft.ControlEvent) -> None:
            info = ft.AlertDialog(
                    title=ft.Row(
                        [
                            ft.Text(Messages.MSG_ABOUT_APP, size=25, weight=ft.FontWeight.W_300,color=ft.Colors.WHITE),
                            ft.IconButton(
                                content=ft.Image(src=IconCustom.ICON_INFO_CIRCLE_FILL, width=20, height=20, color=ft.Colors.WHITE),disabled=True,
                            )
                        ]
                    ),
                    shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(13,13,13,13)),
                    content=ft.Column(
                            [
                                ft.Text("Desarrollado por: Josue Lopez" \
                                "\nBiblioteca gráfica: flet 0.27.2" \
                                "\nLenguaje programación: Python 3.12" \
                                "\nVersión: 1.0.0 ", size=14, weight=ft.FontWeight.W_300,color=ft.Colors.WHITE),
                            ],
                        width=296,
                        height=80,
                    ),
                )
            self.page.open(info)
            self.page.update()
        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_INFO, width=25, height=25, color=ft.Colors.WHITE),
                on_click=about,
                tooltip=Messages.MSG_ABOUT
            )

    def _build_button_minimize(self) -> ft.IconButton:
        def minimized(e:ft.ControlEvent) -> None:
            self.page.window.minimized = True 
            self.page.update()
        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_MINIMIZE, width=25, height=25, color=ft.Colors.WHITE),
                on_click=minimized,
                tooltip=Messages.MSG_MINIMIZE
            )
    
    def _build_button_close(self) -> ft.IconButton:
        def close(e:ft.ControlEvent) -> None:
            self.page.window.close()
            print("La aplicación se ha cerrado correctamente.")

        return ft.IconButton(
                content=ft.Image(src=IconCustom.ICON_CLOSE, width=25, height=25, color=ft.Colors.WHITE),
                on_click=lambda _: close(_),
                tooltip=Messages.MSG_CLOSE
            )