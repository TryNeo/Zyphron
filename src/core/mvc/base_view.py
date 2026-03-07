"""
Flet Base View Class
"""
import threading
import flet as ft
from core.constants import Messages
from .base_controller import FletController

class FletView:
    def __init__(
        self, model=None, content: list = None, controller: FletController = None
    ):
        self.controller = controller
        self.model = model
        self.content = content

    def _build_dialog_callable(self, e: ft.ControlEvent, function_action: callable, *args) -> None:
        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            e.control.update()
        )).start()
        function_action(e,*args)

    def _build_dialog(self,e : ft.ControlEvent,
                                id : int = 0,
                                modal_title : str = "",
                                content : ft.Row | ft.Container | ft.Column = None,
                                function_action : callable = None,
                                width_content : int = 400,
                                height_content : int = 232,
                                message_action : str = Messages.MSG_ADD,
                                function_action_args : list = None,
                                ) -> None:

        def close_modal(e: ft.ControlEvent, modal: ft.AlertDialog) -> None:
            e.control.scale = 0.9
            e.control.opacity = 0.6
            threading.Timer(0.15, lambda: (
                setattr(e.control, 'scale', 1),
                setattr(e.control, 'opacity', 1),
                e.control.update()
            )).start()
            self.controller.page.close(modal)
            self.controller.update()

        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            e.control.update()
        )).start()

        modal = ft.AlertDialog(
            barrier_color=ft.colors.with_opacity(0.65, "black"),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            modal=True,
            elevation=2,
            title=ft.Row(
                controls=[
                    ft.Text(modal_title, size=23, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda e: self.controller.page.close(modal)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(13,13,13,13)),
            content=ft.Container(
                width=width_content,
                height=height_content,
                content=content,
                padding=5,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Row(
                            [
                                ft.Text(message_action,size=14,color=ft.Colors.WHITE),
                            ],
                        ),
                    elevation=5,
                    width=75,
                    on_click=lambda e: self._build_dialog_callable(e,
                                                                function_action,[
                                                                id,
                                                                modal,
                                                                content,function_action_args]),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        color="White",
                        overlay_color="black12",
                    ),
                    animate_scale=ft.animation.Animation(150, "easeOutCubic"),
                    animate_opacity=ft.animation.Animation(150, "easeOutCubic"),
                ),
                ft.ElevatedButton(
                    content=ft.Row(
                            [
                                ft.Text(Messages.MSG_CANCEL,size=14,color=ft.Colors.WHITE),
                            ],
                        ),
                    bgcolor=ft.Colors.GREY_600,
                    elevation=2,
                    width=75,
                    on_click=lambda e: close_modal(e,modal),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(8,8,8,8)),
                        padding=ft.padding.only(left=10,right=20,top=5,bottom=5),
                    ),
                    animate_scale=ft.animation.Animation(150, "easeOutCubic"),
                    animate_opacity=ft.animation.Animation(150, "easeOutCubic"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.controller.page.open(modal)
        self.controller.update()