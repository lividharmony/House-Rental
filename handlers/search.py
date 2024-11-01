from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from aiogram.filters import Command, CommandStart
from bot import dp

router = Router()


@router.message(CommandStart())
async def search_housings(message: types.Message):
    await message.answer("Uy-joylarni qidirish uchun joylashuvni kiriting:")
    await message.set_state("search_location")


@router.message(state="search_location")
async def handle_location(message: types.Message, state: FSMContext):
    location = message.text
    pool = dp['db']
    async with pool.acquire() as connection:
        housings = await connection.fetch(
            "SELECT * FROM housings WHERE location = $1 AND available = TRUE", location
        )

    if not housings:
        await message.answer("Ushbu joylashuvda uy-joylar topilmadi.")
    else:
        response = "Mavjud uy-joylar:\n"
        for housing in housings:
            response += f"{housing['description']} - {housing['price']} USD\n"
        await message.answer(response)
    await state.finish()
