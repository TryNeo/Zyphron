"""
Flet Base Model Class
"""
import os
import sys
import aiosqlite
from typing import Any, Optional
from typing import Any, Dict

class FletModel:
    def __init__(self, **kwargs):
        self.controller = None
        self.nombre_bd : str = "ZyphronDB.db"
        self.rutad_async : str = os.environ.get('userprofile')+r"\Desktop\Zyphron\bd"
        self.ruta_bd_async : str = os.path.join(self.rutad_async, self.nombre_bd)

    async def _execute_query(self, query: str, params: tuple = ()) -> list:
            async with aiosqlite.connect(self.ruta_bd_async, check_same_thread=False) as db:
                async with db.execute(query, params) as cursor:
                    return await cursor.fetchall()
        
    async def _execute_action(self, query: str, params: tuple = ()) -> bool:
        async with aiosqlite.connect(self.ruta_bd_async, check_same_thread=False) as db:
            await db.execute("PRAGMA foreign_keys = ON;")
            await db.execute(query, params)
            await db.commit()
            return True

    async def select_raw(self, sql: str, params: tuple = ()) -> list:
        try:
            return await self._execute_query(sql, params)
        except Exception:
            return []

    async def select_search(self, id: Optional[int], table: str, where: Optional[Dict]) -> Any:
        sql = f"SELECT * FROM {table}"
        params = ()
        if where:
            conditions = [f"{k} = ?" for k in where.keys()]
            sql += " WHERE " + " AND ".join(conditions)
            params = tuple(where.values())
        result = await self._execute_query(sql, params)
        if id is None:
            return result
        if not result or result[0][0] == id:
            return False
        return True

    async def insert(self, table: str, data: Dict[str, Any]) -> bool:
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return await self._execute_action(sql, tuple(data.values()))

    async def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> bool:
        set_clause = ', '.join([f"{k} = ?" for k in data])
        where_clause = ' AND '.join([f"{k} = ?" for k in where])
        sql = f"UPDATE {table} SET {set_clause} , updated_at = CURRENT_TIMESTAMP WHERE {where_clause}"
        return await self._execute_action(sql, tuple(data.values()) + tuple(where.values()))

    async def delete(self, table: str, where: Dict[str, Any]) -> bool:
        where_clause = ' AND '.join([f"{k} = ?" for k in where])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        return await self._execute_action(sql, tuple(where.values()))
    
    async def delete_logic(self, table: str, where: Dict[str, Any]) -> bool:
        set_clause = ' AND '.join([f"{k} = ?" for k in where])
        where_clause = ' AND '.join([f"{k} = ?" for k in where])
        sql = f"UPDATE {table} SET is_active = 0, deleted_at = CURRENT_TIMESTAMP WHERE {where_clause}"
        return await self._execute_action(sql, tuple(where.values()))