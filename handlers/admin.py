from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot import dp
from config import ADMINS

router = Router()


def filter_by_id(message):
    if message.from_user.id in ADMINS:
        return True
    return False


@router.message(Command("add_housing"), filter_by_id)
async def add_housing(message: types.Message):
    await message.answer("Uy-joy haqida ma'lumot kiriting (masalan, narxi, joylashuvi va muddati):")
    await message.set_state("add_housing_description")


@router.message()
async def save_housing(message: types.Message, state: FSMContext):
    description = message.text
    pool = dp['db']

    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO housings (description, price, location, duration, available) VALUES ($1, $2, $3, $4, TRUE)",
            description, 500, "Toshkent", 6
        )
    await message.answer("Uy-joy muvaffaqiyatli qo'shildi!")
    await state.clear()
