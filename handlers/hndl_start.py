from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db_folder import db

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    author_id = message.from_user.id
    user = await db.users.get_user_by_telegram_id(author_id)
    if user is None:
        await message.answer("Привет. Запись о твоём аккаунте не найдена, обратись к администратору @slavi_slavi для создания аккаунта.")
    else:
        await message.answer("Привет")