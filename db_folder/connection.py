
import os
from pathlib import Path
import aiosqlite

CONFIGS_FODLER = Path(__file__).with_name("configs_folder")
DB_PATH = os.path.join(os.path.dirname(__file__), "bot_state.db")


class Database:
    def __init__(self, path: str):
        self.path = path
        self.db: aiosqlite.Connection | None = None

    async def connect(self):
        self.db = await aiosqlite.connect(self.path)
        await self.db.execute("PRAGMA foreign_keys = ON;")

    async def close(self):
        if self.db is not None:
            await self.db.close()
            self.db = None


        
async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:
        async with conn.cursor() as cur:

            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    uuid TEXT NOT NULL,
                    PRIMARY KEY (telegram_id)
                );
            """)


        await conn.commit()