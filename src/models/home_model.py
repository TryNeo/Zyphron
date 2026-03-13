import asyncio
from core.mvc import (FletModel)

class HomeModel(FletModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def get_credentials_async(self) -> list:
        query = """
            SELECT
                id_credential,
                title_credential,
                username,
                passwrd
            FROM credentials WHERE is_active = 1
            ORDER BY title_credential,username
        """
        return await self._execute_query(query)
    
    def get_credentials(self):
        return asyncio.run(self.get_credentials_async())
    
    def search_credentials(self, search_term: str):
        query = """
            SELECT
                id_credential,
                title_credential,
                username,
                passwrd
            FROM credentials
            WHERE is_active = 1 AND (title_credential LIKE ?)
            ORDER BY title_credential,username
        """
        like_term = f"%{search_term}%"
        return asyncio.run(self._execute_query(query, (like_term,)))

    def add_credential(self, title: str, username: str, password: str):
        return asyncio.run(self.insert("credentials", {
            "title_credential": title,
            "username": username,
            "passwrd": password
        }))
    
    def edit_credential(self, id_cred: int, title: str, username: str, password: str):
        return asyncio.run(self.update("credentials", {
            "title_credential": title,
            "username": username,
            "passwrd": password
        }, {"id_credential": id_cred}))

    def delete_credential(self, id_cred: int):
        asyncio.run(self.delete_logic("credentials", {"id_credential": id_cred}))

    async def get_routes_async(self,offset : int,limit: int = 7) -> list:
        query = """
            SELECT
                id_route,
                project,
                title_route,
                path_route
            FROM routes WHERE is_active = 1
            ORDER BY project,title_route
            LIMIT ? OFFSET ?
        """
        return await self._execute_query(query, (limit, offset))
    
    def get_routes(self,offset : int,limit: int = 14):
        return asyncio.run(self.get_routes_async(offset, limit))

    async def get_data_paginate_route_async(self, search: str, offset: int, limit: int = 7) -> list:
        query = """
            SELECT
                id_route,
                project,
                title_route,
                path_route
            FROM routes
            WHERE project LIKE ? OR title_route LIKE ? 
            ORDER BY project, title_route
            LIMIT ? OFFSET ?
        """
        like_search = f"%{search}%"
        return await self._execute_query(query, (like_search, like_search, limit, offset))
    
    def get_data_paginate_route(self, search: str, offset: int, limit: int = 7):
        return asyncio.run(self.get_data_paginate_route_async(search, offset, limit))
    
    async def total_records_route_async(self) -> int:
        query = " SELECT COUNT(*) FROM routes"
        result = await self._execute_query(query)
        return result[0][0] if result else 0
    
    def total_records_route(self) -> int:
        return asyncio.run(self.total_records_route_async())