import threading
import flet as ft
import flet_lottie as fl
from core.constants import Messages
from core.mvc import (FletController)
from urllib.parse import urlparse

class HomeController(FletController):
    def __init__(self, model, page: ft.Page) -> None:
        self.model = model
        self.page = page
        super().__init__(model, page)
        self.content_tabs = self._build_tabs()

    def shorten_url(self,url: str, max_length: int = 60) -> str:
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"

            if len(url) <= max_length:
                return url

            remaining = max_length - len(base) - 4
            if remaining <= 0:
                return base + "/..."

            return base + "/" + url[len(base)+1 : len(base)+1+remaining] + "..."

    def _build_add_route(self) -> ft.Button:
        return ft.Button(
                    height=56,
                    text=Messages.MSG_ADD,
                    icon=ft.icons.ADD,
                    icon_color="white",
                    elevation=5,
                    animate_scale=ft.animation.Animation(150, "easeOutCubic"),
                    animate_opacity=ft.animation.Animation(150, "easeOutCubic"),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        color="White",
                        overlay_color="black12",
                    ),
                )

    def _build_search_routes(self) -> ft.TextField:
        return  ft.TextField(
                    label="Buscar por proyecto o ruta",
                    suffix_icon=ft.icons.SEARCH,
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.GREY_600,
                    max_length=50,
                    show_cursor=True,
                )

    def _build_datatable(self) -> ft.DataTable:
            return ft.DataTable(
                        border=ft.border.all(0.5, ft.Colors.GREY_400),
                        border_radius=2,
                        data_row_color={ft.ControlState.HOVERED: ft.colors.with_opacity(0.8, "#00001B") },
                        heading_row_color="#292929",
                        heading_row_height=28,
                        data_row_min_height=43.5,
                        data_row_max_height=43.5,
                        divider_thickness=45,
                        sort_column_index=0,
                        sort_ascending=True,
                        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_400),
                        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_400),
                        height=335,
                        width=880,
                        columns=[
                            ft.DataColumn(ft.Text("Proyecto", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                            ft.DataColumn(ft.Text("Título", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                            ft.DataColumn(ft.Text("Ruta", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                            ft.DataColumn(ft.Text("Opciones", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text("Nexus", size=14, font_family="SaansRegular", color="#e2e8f0")),
                                    ft.DataCell(ft.Text("Calidad", size=14, font_family="SaansRegular", color="#e2e8f0")),
                                    ft.DataCell(ft.Text(f"{self.shorten_url('https://intranet.corporacion-internacional.local/sistema/gestion-documental/expedientes/2026/marzo/cliente-00045872/documento-contrato-servicios-profesionales-version-final-aprobada?id=45872&hash=9f8a7b6c5d4e3f210987654321abcdefabcdef1234567890fedcba0987654321&verificacion=true')}", size=14, font_family="SaansRegular", color="#97c0f5ff" ,style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE))),
                                    ft.DataCell(
                                        ft.Row(
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.icons.COPY_ALL,
                                                    icon_size=18,
                                                    icon_color=ft.colors.GREY_400,
                                                    tooltip=Messages.MSG_VIEW,
                                                    #on_click=lambda e: print("Ver función no implementada"),
                                                ),
                                                ft.PopupMenuButton(
                                                        tooltip="Opciones",
                                                        icon_color=ft.colors.GREY_400,
                                                        icon=ft.icons.MORE_VERT,
                                                        items=[
                                                            ft.PopupMenuItem(content=ft.Row(
                                                                controls=[
                                                                    ft.Icon(ft.icons.EDIT_OUTLINED, color=ft.colors.GREY_400),
                                                                    ft.Text(Messages.MSG_EDIT, size=14, font_family="SaansRegular", color="#e2e8f0"),
                                                                ],
                                                            ),),
                                                            ft.PopupMenuItem(
                                                                content=ft.Row(
                                                                    controls=[
                                                                        ft.Icon(ft.icons.DELETE_OUTLINE, color="#ef4444"),
                                                                        ft.Text(Messages.MSG_DELETE, size=14, font_family="SaansRegular", color="#e2e8f0"),
                                                                    ],
                                                                ),
                                                            ),
                                                        ],
                                                )
                                            ]
                                        )
                                    ),
                                ],
                            ),
                        ]
                    )

    def _build_paging_buttons(self) -> ft.Row:
        return  ft.Row(
                    controls=[
                        ft.Text(
                            "Mostrando del 1 al 27 de 3160 entradas",
                            color=ft.Colors.WHITE,
                            weight=ft.FontWeight.W_400,
                            size=14
                        ),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                                            icon_color=ft.Colors.WHITE,
                                            tooltip=Messages.MSG_PREVIOUS,
                                            width=40,
                                            height=40,
                                            #on_click=lambda e: self.paginator(e,False)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                            icon_color=ft.Colors.WHITE,
                                            tooltip=Messages.MSG_NEXT,
                                            width=40,
                                            height=40,
                                            #on_click=lambda e: self.paginator(e,True)
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                    #spacing=669,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )

    def _build_tabs(self) -> ft.Tabs:
        def _build_tab_routes()-> ft.Tab:
            return  ft.Tab(
                    text=Messages.MSG_ROUTES,
                    content=ft.Container(
                        padding=20,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        self._build_search_routes(),
                                        self._build_add_route(),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                self._build_datatable(),
                                self._build_paging_buttons(),
                            ]
                        ),
                    ),
                )

        return ft.Tabs(
            selected_index=0,
            animation_duration=300,
            indicator_color="#e2e8f0",
            indicator_thickness=3,
            label_color="#e2e8f0",
            unselected_label_color="#64748b",
            divider_color="transparent",
            overlay_color="transparent",
            tabs=[
                _build_tab_routes(),
            ],
            expand=1,
        )

    def validate_fields_credential(self, e : ft.ControlEvent) -> None:
        value = e.control.value
        if value.strip() == "":
            e.control.error_text = Messages.MSG_FIELD_REQUIRED
            e.control.data = False
            self.update()
            return
        e.control.error_text = None
        e.control.data = True
        self.update()
        
    def add_credential(self,e : ft.ControlEvent,*args) -> None:
        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            self.update()
        )).start()
        modal = list(args)[0][1]
        title,user,passwd = list(args)[0][2].controls
        content = list(args)[0][3][0].content.controls[1].content
        card_credentials = list(args)[0][3][1]
        if not all([title.data, user.data, passwd.data]):
            return
        else:
            if title.value == "":
                title.error_text = Messages.MSG_FIELD_REQUIRED
                title.data = False
                self.update()
                return
            if user.value == "":
                user.error_text = Messages.MSG_FIELD_REQUIRED
                user.data = False
                self.update()
                return
            if passwd.value == "":
                passwd.error_text = Messages.MSG_FIELD_REQUIRED
                passwd.data = False
                self.update()
                return
        self.model.add_credential(title.value, user.value, passwd.value)
        content.controls = []
        content.controls = [
            card_credentials(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in self.model.get_credentials() ] if self.model.get_credentials() else [
            card_credentials(9999, Messages.MSG_NOT_CREDENTIALS_FOUND, "-", "-")
        ]
        self.update()
        self.page.close(modal)

    def edit_credential(self, e : ft.ControlEvent, *args) -> None:
        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            self.update()
        )).start()
        modal = list(args)[0][1]
        title,user,passwd = list(args)[0][2].controls
        id = list(args)[0][3][0]
        content = list(args)[0][3][1].content.controls[1].content
        card_credentials = list(args)[0][3][2]
        if not all([title.data, user.data, passwd.data]):
            return
        else:
            if title.value == "":
                title.error_text = Messages.MSG_FIELD_REQUIRED
                title.data = False
                self.update()
                return
            if user.value == "":
                user.error_text = Messages.MSG_FIELD_REQUIRED
                user.data = False
                self.update()
                return
            if passwd.value == "":
                passwd.error_text = Messages.MSG_FIELD_REQUIRED
                passwd.data = False
                self.update()
                return
        self.model.edit_credential(id,title.value, user.value, passwd.value)
        content.controls = []
        content.controls = [
            card_credentials(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in self.model.get_credentials() ] if self.model.get_credentials() else [
            card_credentials(9999, Messages.MSG_NOT_CREDENTIALS_FOUND, "-", "-")
        ]
        self.update()
        self.page.close(modal)

    def delete_credential(self, e : ft.ControlEvent, 
                          id_cred: int, 
                          content_user_callback,
                          card_credentials_callback) -> None:
        content = content_user_callback.content.controls[1].content
        card_credentials = card_credentials_callback
        if id_cred == 9999:
            return
        self.model.delete_credential(id_cred)
        content.controls = []
        content.controls = [
            card_credentials(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in self.model.get_credentials() ] if self.model.get_credentials() else [
            card_credentials(9999, Messages.MSG_NOT_CREDENTIALS_FOUND, "-", "-")
        ]
        self.update()