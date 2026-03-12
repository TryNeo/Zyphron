"""
Flet Base Controller Class
"""
import flet as ft
import ctypes

from requests.compat import urlparse

from core.ui_constants import Messages
from .base_model import FletModel

class FletController:
    def __init__(self, page: ft.Page, model: FletModel):
        self.page = page
        self.model = model
        self.total_records : int = 0
        self.total_records_pages : int = 0
        self.base_page : int = 0
        self.page_limit : int = 7
        self.current_page : int = 0
        self.search : str = ""

    def update(self) -> None:
        self.page.update()

    def get_user_name(self) -> str:
        size = ctypes.pointer(ctypes.c_ulong(0))
        ctypes.windll.secur32.GetUserNameExW(3, None, size)
        buffer = ctypes.create_unicode_buffer(size.contents.value)
        ctypes.windll.secur32.GetUserNameExW(3, buffer, size)
        full_name = buffer.value
        return full_name

    def shorten_url(self,url: str, max_length: int = 60) -> str:
            parsed = urlparse(url)
            base = f"{parsed.scheme}://{parsed.netloc}"

            if len(url) <= max_length:
                return url

            remaining = max_length - len(base) - 4
            if remaining <= 0:
                return base + "/..."

            return base + "/" + url[len(base)+1 : len(base)+1+remaining] + "..."

    def search_records(self, e: ft.ControlEvent, datatable: ft.DataTable, 
                       paging_buttons: ft.Row , base_page,
                       generate_row_data_func : callable,
                       get_data_func : callable,
                       get_data_paginate_func : callable,
                       get_total_records_func : callable) -> None:
        self.search = e.control.value
        if self.total_records > 0:
            self.generate_records(datatable,paging_buttons,base_page,
                                generate_row_data_func,
                                get_data_func,
                                get_data_paginate_func,
                                get_total_records_func)
            self.update()

    def paginator(self, e: ft.ControlEvent, datatable: ft.DataTable, 
                  paging_buttons: ft.Row, reverse: bool,
                  generate_row_data_func : callable,
                  get_data_func : callable,
                  get_data_paginate_func : callable,
                  get_total_records_func : callable) -> None:
        self.current_page = datatable.data
        if reverse != False:
            self.current_page += 1
            offset = self.current_page * self.page_limit
            if len(get_data_func(offset)) == 0:
                self.current_page -= 1
                self.generate_records(datatable,paging_buttons,self.current_page,
                                    generate_row_data_func,
                                    get_data_func,
                                    get_data_paginate_func,
                                    get_total_records_func)
                self.update()
                return
            self.generate_records(datatable,paging_buttons,self.current_page,
                                generate_row_data_func,
                                get_data_func,
                                get_data_paginate_func,
                                get_total_records_func)
            self.update()
        else:
            if self.current_page > 0:
                self.current_page -= 1
                self.generate_records(datatable,paging_buttons,self.current_page,
                                    generate_row_data_func,
                                    get_data_func,
                                    get_data_paginate_func,
                                    get_total_records_func)
                self.update()

    def generate_records(self, datatable: ft.DataTable, paging_buttons: ft.Row, base_page: int, 
                        generate_row_data_func : callable,
                        get_data_func : callable,
                        get_data_paginate_func : callable,
                        get_total_records_func : callable) -> None:
        datatable.rows.clear()
        datatable.rows = []
        datatable.data = base_page
        offset = base_page * self.page_limit
        if get_data_paginate_func(self.search, offset) is None:
            self.total_records = 0
            self.total_records_page = 0
            self.total_records_pages = 0
            paging_buttons.controls[0].value = f"{Messages.MSG_TOTAL_RECORDS} {self.total_records}"
            return
        else:
            for record in get_data_paginate_func(self.search, offset) or []:
                if len(datatable.rows) == self.page_limit:
                    break
                generate_row_data_func(datatable,record)
            self.total_records = get_total_records_func()
            self.total_records_page = get_data_paginate_func(self.search, offset)
            self.total_records_pages = self.total_records_page 
            if self.total_records_page == 0:
                self.total_records_pages = 0
            else:
                self.total_records_pages = len(self.total_records_page)
            if self.total_records_pages == 0 and offset != 0:
                base_page -= 1
                self.generate_records(datatable,paging_buttons,base_page,
                                    generate_row_data_func,
                                    get_data_func,
                                    get_data_paginate_func,
                                    get_total_records_func)
        paging_buttons.controls[1].controls[0].controls[0].disabled = self.current_page == 0
        paging_buttons.controls[1].controls[0].controls[1].disabled = self.current_page >= self.total_records_pages - 1
        inicio = self.current_page * self.page_limit + 1
        fin = min((self.current_page + 1) * self.page_limit, self.total_records)
        paging_buttons.controls[0].value = f"Mostrando {inicio}-{fin} de {self.total_records} registros"
        self.update()
