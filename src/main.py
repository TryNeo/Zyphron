import locale

import flet as ft
from repath import match
from typing import Final
from controllers import *
from models import *
from views import *
from core.mvc import (FletView,FletModel,FletController)

try:
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
except:
    pass

class MainApplication:
    def __init__(self) -> None:
        self._TITLE      : Final[str] = "Zyphron"
        self._PLATFORMS  : Final[list] = ["android", "ios", "macos", "linux", "windows"]
        self._WIDTH      : Final[int] = 1350
        self._HEIGHT     : Final[int] = 830

    def _configure_app(self, page: ft.Page) -> None:
        def configure_title() -> None:
            page.title = self._TITLE
            page.window.title_bar_buttons_hidden = True
            page.window.title_bar_hidden = True
            page.window.resizable = False

        def configure_window() -> None:
            page.window.center()
            page.window.width  = self._WIDTH
            page.window.height = self._HEIGHT
            page.locale_configuration = ft.LocaleConfiguration(
                supported_locales=
                [
                    ft.Locale(language_code="es", country_code="ES"),
                ],
                current_locale=ft.Locale(language_code="es", country_code="ES"),
            )

        def configure_theme() -> None:
            page.fonts = {
                "SaansRegular":"/fonts/SaansRegular.ttf",
                "SaansBold":"/fonts/SaansBold.ttf",
                "SaansMedium":"/fonts/SaansMedium.ttf",
                "Digii": "fonts/DS-Digii.ttf",
                "Digital": "fonts/DS-Digital.ttf",
            }
            theme = ft.Theme(use_material3=True,
                             font_family="SaansRegular",
                             visual_density=ft.VisualDensity.STANDARD,
                             )
            for platform in self._PLATFORMS:
                setattr(theme.page_transitions, platform, ft.PageTransitionTheme.NONE)
                theme.scrollbar_theme = ft.ScrollbarTheme(
                    track_color={
                        ft.ControlState.FOCUSED: ft.Colors.TRANSPARENT,
                        ft.ControlState.HOVERED: ft.Colors.TRANSPARENT,
                        ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
                    },
                    track_visibility=False,
                    thickness=5,
                    radius=15,
                    main_axis_margin=5,
                )
            #page.theme = theme
            page.bgcolor = ft.Colors.BLACK

        configure_title()
        configure_window()
        configure_theme()

    def _configure_routes(self,page: ft.Page) -> None:
        def path(url: str, clear: bool, view: ft.View, model: FletModel, controller: FletController) -> list:
            return [url, clear, view, model, controller]

        def routes_add() -> list[list]:
            return [
                path(url="/", clear=True, view=HomeView, model=HomeModel, controller=HomeController),
                path(url="/enviroments", clear=True, view=EnviromentsView, model=EnviromentsModel, controller=EnviromentsController),
            ]
        
        def page_add(url: str, view: ft.View, model=FletModel, controller=FletController) -> None:
            model : FletModel = model()
            controller : FletController = controller(page, model)
            model.controller = controller
            view : FletView = view(controller, model, url)
            page.views.append(view.content)
            page.update()


        def routes(e: ft.ControlEvent) -> None:
            for url in routes_add():
                path_match = match(url[0], e.route)
                if path_match:
                    if url[1]:
                        page.views.clear()
                    page_add(url=url[0], view=url[2], model=url[3], controller=url[4])
                    break
        page.on_route_change = routes
        page.go(page.route)


    def __call__(self, flet_page: ft.Page) -> None:
        self.page = flet_page
        self._configure_app(self.page)
        self._configure_routes(self.page)
        
if __name__ == "__main__":
    ft.app(target=MainApplication(),assets_dir="assets")