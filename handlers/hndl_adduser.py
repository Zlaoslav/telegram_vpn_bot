from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db_folder import db
from configs import ADMIN_ID
import uuid

router = Router()

class AddUserStates(StatesGroup):
    waiting_for_telegram_id = State()
    waiting_for_email = State()

@router.message(Command("adduser"))
async def adduser_cmd(message: Message, state: FSMContext):
    author_id = message.from_user.id
    if author_id != ADMIN_ID:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    args = message.text.split()[1:]
    if args:
        if len(args) == 2:
            telegram_id, email = args
            try:
                telegram_id = int(telegram_id)
                email = str(email)
                user_uuid = str(uuid.uuid4())
                success, msg = await db.users.add_user(telegram_id, email, user_uuid)
                if success:
                    await message.answer(f"Пользователь с Telegram ID {telegram_id} добавлен.")
                else:
                    await message.answer(f"Ошибка: {msg}")
            except ValueError:
                await message.answer("Неверные форматы аргументов.")
        else:
            await message.answer("Использование: /adduser <telegram_id> <email> или /adduser для пошагового ввода")
    else:
        await state.set_state(AddUserStates.waiting_for_telegram_id)
        await message.answer("Введите Telegram ID пользователя:")

@router.message(AddUserStates.waiting_for_telegram_id)
async def process_telegram_id(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        await state.update_data(telegram_id=telegram_id)
        await state.set_state(AddUserStates.waiting_for_email)
        await message.answer("Введите email пользователя:")
    except ValueError:
        await message.answer("Неверный Telegram ID. Введите число.")

@router.message(AddUserStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    data = await state.get_data()
    telegram_id = data.get('telegram_id')
    user_uuid = str(uuid.uuid4())
    try:
        success, msg = await db.users.add_user(telegram_id, email, user_uuid)
        if success:
            await message.answer(f"Пользователь с Telegram ID {telegram_id} добавлен.")
        else:
            await message.answer(f"Ошибка: {msg}")
    except Exception as e:
        await message.answer(f"Ошибка при добавлении пользователя: {e}")
    finally:
        await state.clear()