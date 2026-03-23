import flet as ft
from core.header import Header
from core.constants import IconCustom,Messages
from core.mvc import (FletView,FletModel,FletController)

class EnviromentsView(FletView):
    def __init__(self, controller:FletController, model:FletModel,route_url:str):
        self.controller  = controller
        self.model = model
        self.route_url = route_url
        self.view = self._build_view()
        super().__init__(self.model, self.view, self.controller)

    def _build_header(self) -> ft.AppBar:
        return Header(
                    page=self.controller.page,
                    title=Messages.MSG_ENVIRONMENTS,
                    screen_id=1,
                ).build()

    def _build_view(self) -> ft.View:
        return ft.View(
            route=self.route_url,
            controls=[
                #self._build_body(),
            ],
            appbar=self._build_header(),
        )