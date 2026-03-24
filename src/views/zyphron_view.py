import datetime
import random
import pytz
import time
import flet as ft
from core.header import Header
from core.constants import Messages
from core.mvc import (FletView,FletModel,FletController)

class ZyphronView(FletView):
    def __init__(self, controller:FletController, model:FletModel,route_url:str):
        self.controller  = controller
        self.model = model
        self.route_url = route_url
        self.credentials = [
            self._build_card(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in self.model.get_credentials() ] if self.model.get_credentials() else [
            self._build_card(9999, Messages.MSG_NOT_CREDENTIALS_FOUND,"-","-")
        ]
        self.page_limit = 7
        self.content_user = self._build_content_user()
        self.datatable_custom = self._build_datatable(
            columns=[
                ft.DataColumn(ft.Text("Proyecto", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                ft.DataColumn(ft.Text("Título", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                ft.DataColumn(ft.Text("Ruta", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
                ft.DataColumn(ft.Text("Opciones", size=14, weight="bold", font_family="SaansRegular", color="#e2e8f0")),
            ],
        )
        self.paging_buttons = self._build_paging_buttons()
        self.controller.generate_records(
                self.datatable_custom,
                self.paging_buttons,
                self.controller.base_page,
                self.controller.generate_row_data_routes,
                self.model.get_routes,
                self.model.get_data_paginate_route,
                self.model.total_records_route,
                self.page_limit
                )
        self.grid_notes = self._build_grid_notes()
        self.content_tabs = self._build_tabs()
        self.view = self._build_view()
        super().__init__(self.model, self.view, self.controller)

    def _build_header(self) -> ft.AppBar:
        return Header(
                    page=self.controller.page,
                    title=Messages.MSG_PANEL_CONTROL,
                    screen_id=0,
                ).build()

    def _build_view(self) -> ft.View:
        return ft.View(
            route=self.route_url,
            controls=[
                self._build_body(),
            ],
            appbar=self._build_header(),
        )
    
    def _build_body(self) -> ft.Column:
        def _build_clock(title, zone_hour, color_main):
            hour_text = ft.Text(size=60,weight=ft.FontWeight.BOLD,color=color_main,font_family="Digital")
            date_text = ft.Text(size=20,color=color_main,font_family="SaansRegular")
            utc_text = ft.Text(size=14,color=color_main,font_family="SaansRegular")
            container = ft.Container(
                            width=440,
                            height=300,
                            border_radius=5,
                            blur=ft.Blur(12,12,ft.BlurTileMode.DECAL),
                            content=ft.Column(
                                horizontal_alignment="center",
                                controls=[
                                    ft.Text(
                                        title,
                                        size=20,
                                        weight="bold",
                                        font_family="SaansMedium",
                                        color="#e2e8f0",
                                    ),
                                    hour_text,
                                    date_text,
                                    utc_text,
                                ],
                            ),
                       )
            def update_clocks():
                while True:
                    now = datetime.datetime.now(zone_hour)
                    hour_text.value = now.strftime("%H:%M:%S")
                    date_text.value = now.strftime("%A, %d de %B de %Y").encode("latin1").decode("utf-8")
                    different = now.utcoffset().total_seconds() / 3600
                    utc_text.value = f"Zona horaria: UTC {different:+.0f}"
                    container.update()
                    time.sleep(1)
            return container, update_clocks
        
        tz_chile = pytz.timezone("America/Santiago")
        tz_spain = pytz.timezone("Europe/Madrid")
        clock_chile, thread_chile = _build_clock(
            Messages.MSG_CHILE, tz_chile, "#e9e9e9"
        )
        clock_espana, thread_espana = _build_clock(
            Messages.MSG_SPAIN, tz_spain, "#e9e9e9"
        )
        self.controller.page.run_thread(thread_chile)
        self.controller.page.run_thread(thread_espana)

        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        clock_chile,
                                        clock_espana,
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                width=900,
                                height=200,
                            ),
                            ft.Container(
                                content=self.content_tabs,
                                width=900,
                                height=530,
                            )
                        ]
                    )
                ),
                self.content_user,
            ]
        )

    def _build_content_user(self) -> ft.Container:
        return  ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.TextField(
                                        label=Messages.MSG_SEARCH_USER_OR_TITLE,
                                        suffix_icon=ft.icons.SEARCH,
                                        label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                                        border_radius=ft.BorderRadius(10,10,10,10),
                                        border_color=ft.Colors.GREY_600,
                                        max_length=50,
                                        show_cursor=True,
                                        on_change=lambda e: self.controller.search_credentials(e, 
                                                                                               self.content_user,
                                                                                               self._build_card),
                                    ),
                                    ft.Button(
                                        height=56,
                                        text=Messages.MSG_ADD,
                                        icon=ft.icons.ADD,
                                        icon_color="white",
                                        elevation=5,
                                        animate_scale=ft.animation.Animation(150, "easeOutCubic"),
                                        animate_opacity=ft.animation.Animation(150, "easeOutCubic"),
                                        on_click=lambda e:self._build_dialog(e, 
                                                                            modal_title="Agregar credencial",
                                                                            content=ft.Column(
                                                                                controls=[
                                                                                    self._build_title_credential(),
                                                                                    self._build_user_credential(),
                                                                                    self._build_passwd_credential(),
                                                                                ],
                                                                                spacing=15,
                                                                            ),
                                                                            function_action=self.controller.add_credential,
                                                                            function_action_args=[
                                                                                self.content_user,
                                                                                self._build_card,
                                                                            ]
                                                                            ),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=5),
                                            color="White",
                                            overlay_color="black12",
                                        ),
                                    )
                                ],
                            ),
                            ft.Container(
                                height=650,
                                width=400,
                                content=ft.Column(
                                    expand=True,
                                    scroll=ft.ScrollMode.AUTO,
                                    controls=self.credentials,
                                )
                            )
                        ]
                    ),
                    width=400,
                    height=730,
            )

    def _build_card(self, id:int, title: str, user: str, passwd : str) -> ft.Card:
        def show_message(text: str):
            self.controller.page.snack_bar = ft.SnackBar(
                content=ft.Row([
                    ft.Icon(ft.icons.INFO,color=ft.colors.BLACK),
                    ft.Text(text)
                ]),
                duration=2000,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                show_close_icon=True
            )
            self.controller.page.open(self.controller.page.snack_bar)
            self.controller.update()

        def _build_card_header(title: str) -> ft.Row:
            return ft.Row(
                alignment="spaceBetween",
                controls=[
                    ft.Text(
                        title,
                        size=17,
                        font_family="SaansRegular",
                        weight="bold",
                        color="white",
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
                                ),
                                on_click=lambda e: self._build_dialog(e,
                                                                modal_title="Editar credencial",
                                                                content=ft.Column(
                                                                        controls=[
                                                                            self._build_title_credential(title),
                                                                            self._build_user_credential(user),
                                                                            self._build_passwd_credential(passwd),
                                                                        ],
                                                                        spacing=15,
                                                                ),
                                                                function_action=self.controller.edit_credential,
                                                                function_action_args=[
                                                                    id,
                                                                    self.content_user,
                                                                    self._build_card,
                                                                ],
                                                                message_action=Messages.MSG_SAVE,
                                                        ),
                                ),
                                ft.PopupMenuItem(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.DELETE_OUTLINE, color="#ef4444"),
                                            ft.Text(Messages.MSG_DELETE, size=14, font_family="SaansRegular", color="#e2e8f0"),
                                        ],
                                    ),
                                    on_click=lambda e: 
                                            self.controller.delete_credential(e, id, 
                                                                        self.content_user,self._build_card),
                                ),
                            ],
                    ),
                ],
            )

        def _build_card_username(user: str) -> ft.Row:
            return ft.Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                Messages.MSG_USER,
                                size=11,
                                weight="bold",
                                font_family="SaansRegular",
                                color="#64748b",
                            ),
                            ft.Text(
                                user,
                                size=15,
                                font_family="SaansRegular",
                                color="#e2e8f0",
                            ),
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.icons.CONTENT_COPY,
                        icon_size=18,
                        icon_color=ft.colors.GREY_400,
                        tooltip=Messages.MSG_COPY_USER,
                        on_click=lambda e: (self.controller.page.set_clipboard(user), show_message("Usuario copiado al portapapeles")),
                    ),
                ],
            )

        def _build_card_password(passwd: str) -> ft.Row:
            visible = False
            password_text = ft.Text("•••••••••••••", size=15,font_family="SaansRegular",
                                color="#e2e8f0",)

            def toggle_password(e):
                nonlocal visible
                visible = not visible
                password_text.value = passwd if visible else "•••••••••••••"
                e.control.icon = (
                    ft.icons.VISIBILITY_OFF if visible else ft.icons.VISIBILITY
                )
                card.update()

            return ft.Row(
                alignment="spaceBetween",
                vertical_alignment="center",
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(
                                Messages.MSG_PASSWORD,
                                size=11,
                                weight="bold",
                                font_family="SaansRegular",
                                color="#64748b",
                            ),
                            password_text,
                        ],
                    ),
                    ft.Row(
                        spacing=2,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.VISIBILITY,
                                icon_size=18,
                                tooltip=Messages.MSG_SHOW,
                                icon_color=ft.colors.GREY_400,
                                on_click=lambda e: toggle_password(e),
                            ),
                            ft.IconButton(
                                icon=ft.icons.KEY_OUTLINED,
                                icon_size=18,
                                tooltip=Messages.MSG_COPY_PASSWORD,
                                icon_color=ft.colors.GREY_400,
                                on_click=lambda e: (self.controller.page.set_clipboard(passwd), show_message("Contraseña copiada al portapapeles")),
                            ),
                        ],
                    ),
                ],
            )
        
        card = ft.Card(
                    elevation=3,
                    shape=ft.RoundedRectangleBorder(radius=7),
                    content=ft.Container(
                        padding=16,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                # HEADER
                                _build_card_header(title),
                                # USUARIO
                                _build_card_username(user),
                                # PASSWORD
                                _build_card_password(passwd),
                            ],
                        ),
                    ),
                )
        
        return  card
    
    def _build_title_credential(self, value: str = "") -> ft.TextField:
        return  ft.TextField(
                    label="Título de la credencial",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=20,
                    prefix_icon=ft.Icons.TITLE,
                    show_cursor=True,
                    data=True,
                    value=value,
                    on_change=lambda e: self.controller.validate_fields_credential(e),
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
                )

    def _build_user_credential(self, value: str = "") -> ft.TextField:
        return  ft.TextField(
                    label="Usuario",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=20,
                    prefix_icon=ft.Icons.PERSON,
                    show_cursor=True,
                    data=True,
                    value=value,
                    on_change=lambda e: self.controller.validate_fields_credential(e),
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
                )

    def _build_passwd_credential(self, value: str = "") -> ft.TextField:
        return  ft.TextField(
                    label="Contraseña",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=50,
                    prefix_icon=ft.Icons.PASSWORD,
                    show_cursor=True,
                    data=True,
                    value=value,
                    on_change=lambda e: self.controller.validate_fields_credential(e),
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
                )

    def _build_datatable(self, columns) -> ft.DataTable:
        return ft.DataTable(
                    border=ft.border.all(0.5, ft.Colors.WHITE),
                    border_radius=2,
                    data_row_color={ft.ControlState.HOVERED: ft.colors.with_opacity(0.3, "#FFFFFF") },
                    heading_row_height=28,
                    heading_row_color=ft.colors.with_opacity(0.3, "#000000"),
                    data_row_min_height=43.5,
                    data_row_max_height=43.5,
                    #divider_thickness=45,
                    sort_column_index=0,
                    sort_ascending=True,
                    #vertical_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_400),
                    #horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_400),
                    height=335,
                    width=880,
                    columns=columns,
                    rows=[]
                )

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

    def _build_search_routes(self,label: str = "") -> ft.TextField:
        return  ft.TextField(
                    label=label,
                    suffix_icon=ft.icons.SEARCH,
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=50,
                    show_cursor=True,
                    on_change=lambda e: self.controller.search_records(e,
                                                                    self.datatable_custom,
                                                                    self.paging_buttons,
                                                                    self.controller.base_page,
                                                                    self.controller.generate_row_data_routes,
                                                                    self.model.get_routes,
                                                                    self.model.get_data_paginate_route,
                                                                    self.model.total_records_route,
                                                                    self.page_limit),
                )

    def _build_paging_buttons(self) -> ft.Row:
        return  ft.Row(
                    controls=[
                        ft.Text(f"{Messages.MSG_TOTAL_RECORDS} {self.controller.total_records}",size=15,weight=ft.FontWeight.W_300),
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
                                            on_click=lambda e: self.controller.paginator(e,self.datatable_custom,self.paging_buttons,False,
                                                                                         self.controller.generate_row_data_routes,
                                                                                         self.model.get_routes,
                                                                                         self.model.get_data_paginate_route,
                                                                                         self.model.total_records_route,
                                                                                         self.page_limit),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                                            icon_color=ft.Colors.WHITE,
                                            tooltip=Messages.MSG_NEXT,
                                            width=40,
                                            height=40,
                                            on_click=lambda e: self.controller.paginator(e,self.datatable_custom,self.paging_buttons,True,
                                                                                         self.controller.generate_row_data_routes,
                                                                                         self.model.get_routes,
                                                                                         self.model.get_data_paginate_route,
                                                                                         self.model.total_records_route,
                                                                                         self.page_limit),
                                        ),
                                    ]
                                ),
                            ],
                        )
                    ],
                    #spacing=669,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )

    def _build_tab_routes(self)-> ft.Tab:
        return  ft.Tab(
                text=Messages.MSG_ROUTES,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    self._build_search_routes("Buscar por proyecto o ruta"),
                                    #self._build_add_route(),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            self.datatable_custom,
                            self.paging_buttons,
                        ]
                    ),
                ),
            )
    
    def _build_tab_documents(self) -> ft.Tab:
        return  ft.Tab(
                text="Documentos",
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Text("Proximomente se mostrará una lista de documentos con su respectiva información, como el tipo de archivo, tamaño y fecha de creación. Además, se podrán realizar acciones como abrir el documento, eliminarlo o copiar su ruta al portapapeles.", size=14, font_family="SaansRegular", color="#e2e8f0"),
                        ]
                    ),
                ),
            )

    def _build_search_notes(self,label: str = "") -> ft.TextField:
        return  ft.TextField(
                    label=label,
                    suffix_icon=ft.icons.SEARCH,
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=100,
                    width=600,
                    show_cursor=True,
                    on_change=lambda e: self.controller.search_notes(e, 
                                                                    self.grid_notes,
                                                                    self._build_card_note,
                                                                    ),
                )
    
    def _build_title_note(self, value: str = "") -> ft.TextField:
        return  ft.TextField(
                    label="Título de la nota",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    border_radius=ft.BorderRadius(10,10,10,10),
                    border_color=ft.Colors.WHITE,
                    max_length=50,
                    prefix_icon=ft.Icons.TITLE,
                    show_cursor=True,
                    data=True,
                    value=value,
                    #on_change=lambda e: self.controller.validate_fields_note(e),
                    content_padding=ft.padding.symmetric(horizontal=15, vertical=10),
                )
    
    def _build_node_textfield(self, value: str = "") -> ft.TextField:
        return  ft.TextField(
                    label="Contenido de la nota",
                    label_style=ft.TextStyle(color=ft.Colors.WHITE,font_family="SaansRegular"),
                    multiline=True,
                    expand=True,
                    border=ft.InputBorder.NONE,
                    text_style=ft.TextStyle(font_family="SaansRegular", size=14),
                    content_padding=15,
                    value=value,
                    #on_change=lambda e: self.controller.validate_fields_note(e),
                )
    
    def _build_node_content(self, value: str = "") -> ft.Container:
        return ft.Container(
                height=310,
                border=ft.border.all(1, ft.Colors.WHITE),
                border_radius=8,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                content=self._build_node_textfield(value)
        )
    
    def _build_card_note(self, id_note: int, title: str, content: str) -> ft.Card:
        def color_random_soft():
            r = random.randint(80, 220)
            g = random.randint(80, 220)
            b = random.randint(80, 220)
            return f"#{r:02x}{g:02x}{b:02x}"
        
        return ft.Card(
                    show_border_on_foreground=True,
                    shape=ft.RoundedRectangleBorder(radius=1),
                    content=ft.Container(
                        width=400,
                        height=140,
                        padding=15,
                        border=ft.border.only(left=ft.BorderSide(2, color_random_soft()),),
                        content=ft.Column(
                            [
                                ft.Row(
                                    alignment="spaceBetween",
                                    controls=[
                                        ft.Text(f"{self.controller.shorten_text(title,30)}", weight="bold"),
                                        ft.Row(
                                            alignment=ft.MainAxisAlignment.END,
                                            controls=[
                                                ft.IconButton(
                                                    icon=ft.Icons.EDIT_OUTLINED,
                                                    tooltip="Editar nota",
                                                    icon_color=ft.colors.GREY_400,
                                                    on_click=lambda e: self._build_dialog(e,
                                                                modal_title="Editar nota",
                                                                width_content=900,
                                                                height_content=400,
                                                                content=ft.Column(
                                                                        controls=[
                                                                            self._build_title_note(title),
                                                                            self._build_node_content(content),
                                                                        ],
                                                                        tight=True,
                                                                        spacing=10
                                                                ),
                                                                function_action=self.controller.edit_note,
                                                                function_action_args=[
                                                                    id_note,
                                                                    self.grid_notes,
                                                                    self._build_card_note,
                                                                ],
                                                                message_action=Messages.MSG_SAVE,
                                                        ),
                                                ),
                                                ft.IconButton(
                                                    icon=ft.Icons.DELETE_OUTLINE,
                                                    icon_color=ft.colors.RED,
                                                    tooltip="Eliminar nota",
                                                    on_click=lambda e: self.controller.delete_note(e, id_note, 
                                                                                                   self.grid_notes, 
                                                                                                   self._build_card_note),
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                ft.Text(f"{self.controller.shorten_text(content, 120)}"),
                            ]
                        ),
                    ),
                    elevation=3,
                )

    def _build_add_notes(self) -> ft.Button:
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
                    on_click=lambda e: self._build_dialog(e, 
                                        modal_title="Agregar nota",
                                        width_content=900,
                                        height_content=400,
                                        content=ft.Column(
                                            controls=[
                                                self._build_title_note(),
                                                self._build_node_content(),
                                            ],
                                            tight=True,
                                            spacing=10
                                        ),
                                        function_action=self.controller.add_note,
                                        function_action_args=[
                                            self.grid_notes,
                                            self._build_card_note,
                                        ]
                                    ),
                )

    def _build_grid_notes(self) -> ft.Row:
        return ft.Row(
                    wrap=True,
                    spacing=13,
                    alignment=ft.MainAxisAlignment.START,
                    tight=True,
                    run_spacing=10,
                    auto_scroll=True,
                    controls=[self._build_card_note(i[0], i[1], i[2]) for i in self.model.get_notes()],
                )
    
    def _build_tab_notas(self) -> ft.Tab:
        return  ft.Tab(
                text=Messages.MSG_NOTES,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    self._build_search_notes("Buscar por título o contenido"),
                                    self._build_add_notes(),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(
                                height=375,
                                width=880,
                                content=ft.Column(
                                    expand=True,
                                    scroll=ft.ScrollMode.AUTO,
                                    controls=[
                                        self.grid_notes,
                                    ],
                                )
                            )
                        ]
                    ),
                ),
            )

    def _build_tabs(self) -> ft.Tabs:
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
                self._build_tab_routes(),
                self._build_tab_notas(),
            ],
            expand=1,
    )
