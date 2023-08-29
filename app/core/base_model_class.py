from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_cursor
from pydantic import validator


class BaseModelClass(SQLModel):

    @staticmethod
    async def get_cursor():
        return await get_cursor()
#     conn: Connection
#
#     async def _get_cursor(self):
#         if not db.is_connected:
#             conn = await db.connect()
#         return conn or None
