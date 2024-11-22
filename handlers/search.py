
import json
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from handlers.keyboards import cancel_kb, admin_kb, app_inline_kb

from database import create_db_pool
from aiogram.types import Message
from handlers.states import SearchState


router = Router()


@router.message(F.text == "🔙 Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        "Bekor qilindi",
        reply_markup=await admin_kb(message.from_user.id),
    )


@router.message(F.text == "🔍 Search")
async def start_search(message: Message, state: FSMContext):
    await message.answer("Qidiruv 🖋:", reply_markup=cancel_kb())
    await state.set_state(SearchState.search_query)


@router.message(SearchState.search_query)
async def handle_search_query(message: Message, state: FSMContext):
    search_query = message.text
    pool = await create_db_pool()

    async with pool.acquire() as connection:
        housings = await connection.fetch(
            "SELECT id, description, price, location, duration FROM housings "
            "WHERE description ILIKE $1 OR price::text ILIKE $1",
            f"%{search_query}%"
        )

    if not housings:
        await message.answer("❌ Hech narsa topilmadi.")
    else:
        for housing in housings:
            housing_id = housing.get('id')
            if not housing_id:
                await message.answer("Housing ID is missing.")
                continue

            location = housing['location']
            if location:
                try:
                    location_data = json.loads(location)
                    latitude = location_data.get('latitude')
                    longitude = location_data.get('longitude')

                    if latitude and longitude:
                        location_url = f"https://maps.google.com/?q={latitude},{longitude}"
                        location_text = f"[View on Google Maps]({location_url})"
                    else:
                        location_text = "Bu locatsiya ma'lumoti to'liq emas"
                except json.JSONDecodeError:
                    location_text = "⚠️Bu locatsiya ma'lumoti yaroqsiz"
            else:
                location_text = "⚠️Locatsiya taqdim etilmadi."

            await message.answer(
                f"Description🟰 {housing['description']}\n"
                f"Price🟰 {housing['price']} USD\n"
                f"Duration🟰 {housing['duration']} months\n"
                f"Location🟰 {location_text}",
                reply_markup=app_inline_kb(housing_id)
            )
    await state.clear()
