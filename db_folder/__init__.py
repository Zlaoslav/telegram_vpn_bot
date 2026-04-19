import os
import aiosqlite
from typing import Self

from .connection import Database, init_db
from .db_users import UsersRepository
DB_PATH = os.path.join(os.path.dirname(__file__), "bot_state.db")

class DB:
    users: UsersRepository
    def __init__(self):
        self.database = Database(DB_PATH)

    async def __init_repos(self) -> None:
        db: aiosqlite.Connection = self.database.db

        self.users = UsersRepository(db)

        
    async def init_db(self):
        await init_db()

        

    async def connect(self) -> None:
        await self.database.connect()
        await self.__init_repos()

    async def close(self) -> None:
        await self.database.close()

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

# глобальный экземпляр
db = DB()
