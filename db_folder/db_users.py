import aiosqlite
from typing import Optional, Tuple


class UsersRepository:
    __TABLE = "users"

    def __init__(self, db: aiosqlite.Connection):
        self.db = db

    async def add_user(
        self,
        telegram_id: int,
        email: str,
        uuid: str
    ) -> Tuple[bool, str]:
        """Добавляет пользователя в таблицу users."""

        # Проверить, существует ли уже
        existing = await self.get_user_by_telegram_id(telegram_id)
        if existing:
            return False, "Пользователь с таким Telegram ID уже существует"

        existing_uuid = await self.get_user_by_uuid(uuid)
        if existing_uuid:
            return False, "Пользователь с таким UUID уже существует"

        await self.db.execute(
            f"""
                INSERT INTO {self.__TABLE} (telegram_id, email, uuid)
                VALUES (?, ?, ?)
            """,
            (telegram_id, email, uuid)
        )
        await self.db.commit()
        return True, ""


    async def remove_user_by_telegram_id(
        self,
        telegram_id: int
        ) -> Tuple[bool, str]:
        """Удаляет пользователя из таблицы users."""

        existing = await self.get_user_by_telegram_id(telegram_id)
        if not existing:
            return False, "Пользователь с таким Telegram ID не найден"

        await self.db.execute(
            f"""
                DELETE FROM {self.__TABLE}
                WHERE telegram_id = ?
            """,
            (telegram_id,)
        )
        await self.db.commit()
        return True, ""

    async def remove_user_by_uuid(
        self,
        uuid: str
        ) -> Tuple[bool, str]:
        """Удаляет пользователя из таблицы users."""

        existing = await self.get_user_by_uuid(uuid)
        if not existing:
            return False, "Пользователь с таким UUID не найден"

        await self.db.execute(
            f"""
                DELETE FROM {self.__TABLE}
                WHERE uuid = ?
            """,
            (uuid,)
        )
        await self.db.commit()
        return True, ""
    

    async def get_user_by_telegram_id(
        self,
        telegram_id: int
        ) -> Optional[tuple]:
        """Получает информацию о пользователе."""

        cursor = await self.db.execute(
            f"""
                SELECT telegram_id, email, uuid
                FROM {self.__TABLE}
                WHERE telegram_id = ?
            """,
            (telegram_id,)
        )
        return await cursor.fetchone()


    async def get_user_by_uuid(
        self,
        uuid: str
        ) -> Optional[tuple]:
        """Получает информацию о пользователе."""

        cursor = await self.db.execute(
            f"""
                SELECT telegram_id, email, uuid
                FROM {self.__TABLE}
                WHERE uuid = ?
            """,
            (uuid,)
        )
        return await cursor.fetchone()


    async def get_all_users(self) -> list[tuple]:
        """Получает всех пользователей."""

        cursor = await self.db.execute(
            f"""
                SELECT telegram_id, email, uuid
                FROM {self.__TABLE}
            """
        )
        return await cursor.fetchall()
