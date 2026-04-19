from aiogram import Bot, Dispatcher
from configs import TELEGRAM_TOKEN
from handlers import register_handlers
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio
from db_folder import db
from services.hlpr_logging import logger

session = AiohttpSession(proxy="http://127.0.0.1:2080")
bot = Bot(token=TELEGRAM_TOKEN, session=session)
dispatcher = Dispatcher()


async def main():
    await db.init_db()
    async with db:
        register_handlers(dispatcher)
        logger.info(f"Logged as {(await bot.get_me()).username}")
        await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
