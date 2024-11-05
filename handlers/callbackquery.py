import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database import create_db_pool


router = Router()


@router.callback_query(F.data == "accept_housing")
async def confirm_housing(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logging.info("Data in confirm_housing: %s", data)

    description = data.get("description")
    price = data.get("price")
    photo = data.get("photo")
    location = data.get("location")
    duration = data.get("duration")
    print("description", description, "price", price, "location", location)

    if None in (description, price, photo, location, duration):
        await callback.answer("Ma'lumotlar to'liq emas. Iltimos, qaytadan urinib ko'ring.")
        return

    pool = await create_db_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO housings (description, price, photo, location, duration, available)"
            " VALUES ($1, $2, $3, $4, $5, TRUE)",
            description, price, photo, location, duration
        )
    await callback.message.edit_text("Uy-joy muvaffaqiyatli qo'shildi!")
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "reject_housing")
async def reject_housing(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Ma'lumotlar bekor qilindi.")
    await callback.answer()
