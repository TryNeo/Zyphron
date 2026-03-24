import threading
import flet as ft
import flet_lottie as fl
from core.constants import Messages
from core.mvc import (FletController)

class ZyphronController(FletController):
    def __init__(self, model, page: ft.Page) -> None:
        self.model = model
        self.page = page
        super().__init__(model, page)

    def search_credentials(self, e : ft.ControlEvent,content_user_callback,
                          card_credentials_callback) -> None:
        query = e.control.value.strip().lower()
        content = content_user_callback.content.controls[1].content
        card_credentials = card_credentials_callback
        if query == "":
            content.controls = []
            content.controls = [
                card_credentials(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in self.model.get_credentials() ] if self.model.get_credentials() else [
                card_credentials(9999, Messages.MSG_NOT_CREDENTIALS_FOUND, "-", "-")
            ]
            self.update()
            return
        filtered = self.model.search_credentials(query)
        content.controls = []
        content.controls = [
            card_credentials(id_cred, title_cred, user, passwd) for id_cred, title_cred, user, passwd in filtered ] if filtered else [
            card_credentials(9999, Messages.MSG_NOT_CREDENTIALS_FOUND, "-", "-")
        ]
        self.update()

    def search_notes(self, e : ft.ControlEvent, content_notes_callback, note_callback) -> None:
        query = e.control.value.strip().lower()
        content = content_notes_callback
        notes = note_callback
        if query == "":
            content.controls = []
            content.controls = [
                notes(i[0], i[1], i[2]) for i in self.model.get_notes()
            ]
            self.update()
            return
        filtered = self.model.search_notes(query)
        content.controls = []
        content.controls = [
            notes(i[0], i[1], i[2]) for i in filtered
        ]
        self.update()

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

    def add_note(self,e : ft.ControlEvent,*args) -> None:
        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            self.update()
        )).start()
        modal = list(args)[0][1]
        title,note = list(args)[0][2].controls
        content = list(args)[0][3][0]
        notes = list(args)[0][3][1]
        if not all([title.data]):
            return
        else:
            if title.value == "":
                title.error_text = Messages.MSG_FIELD_REQUIRED
                title.data = False
                self.update()
                return
        self.model.add_note(title.value, note.content.value)
        content.controls = []
        content.controls = [
            notes(i[0], i[1], i[2]) for i in self.model.get_notes()
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

    def edit_note(self, e : ft.ControlEvent, *args) -> None:
        e.control.scale = 0.9
        e.control.opacity = 0.6
        threading.Timer(0.15, lambda: (
            setattr(e.control, 'scale', 1),
            setattr(e.control, 'opacity', 1),
            self.update()
        )).start()
        modal = list(args)[0][1]
        title,note = list(args)[0][2].controls
        id = list(args)[0][3][0]
        content = list(args)[0][3][1]
        notes = list(args)[0][3][2]
        if not all([title.data]):
            return
        self.model.edit_note(id,title.value, note.content.value)
        content.controls = []
        content.controls = [
            notes(i[0], i[1], i[2]) for i in self.model.get_notes()
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

    def delete_note(self, e : ft.ControlEvent,
                    id_note: int,
                    content_notes_callback,
                    note_callback) -> None:
        content = content_notes_callback
        notes = note_callback
        self.model.delete_note(id_note)
        content.controls = []
        content.controls = [
            notes(i[0], i[1], i[2]) for i in self.model.get_notes()
        ]
        self.update()

    def copy_url(self, e : ft.ControlEvent, url: str) -> None:
        self.page.set_clipboard(url)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.icons.INFO,color=ft.colors.BLACK),
                ft.Text("URL copiada al portapapeles", color=ft.colors.BLACK)
            ]),
            duration=2000,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            show_close_icon=True
        )
        self.page.open(self.page.snack_bar)
        self.update()

    def generate_row_data_routes(self, 
                        datatable : ft.DataTable ,
                        record : list) -> None:
        datatable.rows.append(
            ft.DataRow(
                on_select_changed=lambda e : None,
                cells=[
                    ft.DataCell(ft.Text(record[1], size=14, font_family="SaansRegular", color="#e2e8f0")),
                    ft.DataCell(content=ft.Container(
                        width=140,
                        content=ft.Text(record[2], size=14, font_family="SaansRegular", color="#e2e8f0"),
                    )),
                    ft.DataCell(
                        ft.Text(f"{self.shorten_url(record[3], 55)}", size=14, font_family="SaansRegular", color="#97c0f5ff" ,style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)),
                        on_tap=lambda e, url=record[3]: self.page.launch_url(url)
                    ),
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.COPY_ALL,
                                    icon_size=18,
                                    icon_color=ft.colors.GREY_400,
                                    tooltip=Messages.MSG_COPY,
                                    on_click=lambda e, url=record[3]: self.copy_url(e, url)
                                ),
                                #ft.IconButton(
                                #    icon=ft.icons.EDIT,
                                #    icon_size=18,
                                #    icon_color=ft.colors.WHITE,
                                #    tooltip=Messages.MSG_EDIT,
                                #    #on_click=lambda e: print("Ver función no implementada"),
                                #),
                                #ft.IconButton(
                                #    icon=ft.icons.DELETE_OUTLINE,
                                #    icon_size=18,
                                #    icon_color=ft.colors.RED,
                                #    tooltip=Messages.MSG_DELETE,
                                #    #on_click=lambda e: print("Ver función no implementada"),
                                #),
                            ]
                        )
                    ),            
                ]
            )
        )