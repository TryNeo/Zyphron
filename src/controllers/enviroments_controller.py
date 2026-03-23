import flet as ft
from core.constants import Messages
from core.mvc import (FletController)

class EnviromentsController(FletController):
    def __init__(self, model, page: ft.Page) -> None:
        self.model = model
        self.page = page
        super().__init__(model, page)