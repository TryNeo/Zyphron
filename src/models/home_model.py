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