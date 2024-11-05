from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from handlers.keyboards import cancel_kb, admin_kb

from database import create_db_pool
from aiogram.types import Message
from handlers.states import SearchState


router = Router()


@router.message(F.text == "Bekor qilish")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    await state.clear()

    await message.answer(
        "Bekor qilindi",
        reply_markup=await admin_kb(message.from_user.id),
    )



@router.message(F.text == "Search")
async def start_search(message: Message, state: FSMContext):
    await message.answer("Qidiruv:", reply_markup=cancel_kb())
    await state.set_state(SearchState.search_query)


@router.message(SearchState.search_query)
async def handle_search_query(message: Message, state: FSMContext):
    search_query = message.text
    pool = await create_db_pool()

    async with pool.acquire() as connection:
        housings = await connection.fetch(
            "SELECT description, price, location, duration FROM housings "
            "WHERE location ILIKE $1 OR price::text ILIKE $1",
            f"%{search_query}%"
        )
    if not housings:
        await message.answer("Hech narsa topilmadi.")
    else:
        for housing in housings:
            await message.answer(
                f"Description: {housing['description']}\n"
                f"Price: {housing['price']} UZS\n"
                f"Location: {housing['location']}\n"
                f"Duration: {housing['duration']} months"
            )

    await state.clear()
