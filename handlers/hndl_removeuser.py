from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db_folder import db
from configs import ADMIN_ID

router = Router()

class RemoveUserStates(StatesGroup):
    waiting_for_telegram_id = State()

@router.message(Command("removeuser"))
async def removeuser_cmd(message: Message, state: FSMContext):
    author_id = message.from_user.id
    if author_id != ADMIN_ID:
        await message.answer("У вас нет прав на выполнение этой команды.")
        return

    args = message.text.split()[1:]
    if args:
        if len(args) == 1:
            try:
                telegram_id = int(args[0])
                success, msg = await db.users.remove_user_by_telegram_id(telegram_id)
                if success:
                    await message.answer(f"Пользователь с Telegram ID {telegram_id} удален.")
                else:
                    await message.answer(f"Ошибка: {msg}")
            except ValueError:
                await message.answer("Неверный Telegram ID.")
        else:
            await message.answer("Использование: /removeuser <telegram_id> или /removeuser для пошагового ввода")
    else:
        await state.set_state(RemoveUserStates.waiting_for_telegram_id)
        await message.answer("Введите Telegram ID пользователя для удаления:")

@router.message(RemoveUserStates.waiting_for_telegram_id)
async def process_remove_telegram_id(message: Message, state: FSMContext):
    try:
        telegram_id = int(message.text)
        success, msg = await db.users.remove_user_by_telegram_id(telegram_id)
        if success:
            await message.answer(f"Пользователь с Telegram ID {telegram_id} удален.")
        else:
            await message.answer(f"Ошибка: {msg}")
    except ValueError:
        await message.answer("Неверный Telegram ID. Введите число.")
    finally:
        await state.clear()