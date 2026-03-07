"""
Flet Base Controller Class
"""
import flet as ft
import ctypes
from .base_model import FletModel

class FletController:
    def __init__(self, page: ft.Page, model: FletModel):
        self.page = page
        self.model = model

    def update(self) -> None:
        self.page.update()

    def get_user_name(self) -> str:
        size = ctypes.pointer(ctypes.c_ulong(0))
        ctypes.windll.secur32.GetUserNameExW(3, None, size)
        buffer = ctypes.create_unicode_buffer(size.contents.value)
        ctypes.windll.secur32.GetUserNameExW(3, buffer, size)
        full_name = buffer.value
        return full_name
