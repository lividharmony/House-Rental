import types

from aiogram import Router
from aiogram.fsm.context import FSMContext

from database import create_db_pool

router = Router()


@router.message(lambda message: message.text == "Listings")
async def search_housings(message: types.Message, state: FSMContext):
    await message.answer("Uy-joylarni qidirish uchun joylashuvni kiriting:")
    await state.set_state("search_location")


@router.message(state="search_location")
async def handle_location(message: types.Message, state: FSMContext):
    location = message.text
    pool = await create_db_pool()

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

    await state.clear()
