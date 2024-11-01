from aiogram import types, Router, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_user_type = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Student"), KeyboardButton(text="Owner")]
    ], resize_keyboard=True
),


async def start_registration(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer("Xush kelibsiz! Ro'yxatdan o'tish uchun telefon raqamingizni kiriting.")
    await state.set_state("phone_number")


async def handle_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone=phone_number)
    await message.answer("Siz Studentmisiz yoki Owner?", reply_markup=choose_user_type)
    await state.set_state("user_type")


async def handle_user_type(message: types.Message, state: FSMContext, dispatcher: Dispatcher, bot: Bot):
    user_type = message.text.lower()
    user_data = await state.get_data()
    pool = bot['db']
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO users (phone, user_type) VALUES ($1, $2) ON CONFLICT (phone) DO NOTHING",
            user_data["phone"], user_type
        )
    await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
    await state.finish()
