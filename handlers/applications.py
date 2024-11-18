from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from .keyboards import admin_kb
from .register import start_registration

router = Router()


@router.message(CommandStart())
async def apply_for_housing(message: types.Message, dispatcher: Dispatcher, state: FSMContext):
    await state.clear()
    housing_id = 1
    user_id = message.from_user.id
    pool = dispatcher['db']
    async with pool.acquire() as connection:
        result = await connection.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)

        if result is None:
            await start_registration(message, state)
            return

    # try:
    #     async with pool.acquire() as connection:
    #         await connection.execute(
    #             "INSERT INTO applications (user_id, housing_id) VALUES ($1, $2)",
    #             user_id, housing_id
    #         )
    #         await bot.send_message(
    #             ADMINS,
    #             f"Yangi ariza tushdi!\nFoydalanuvchi ID: {user_id}, Uy-joy ID: {housing_id}"
    #         )
    #         await message.answer("Arizangiz qabul qilindi!")
    #
    # except Exception as e:
    #     await message.answer("Arizangizni jo'natishda xato yuz berdi.")
    #     print(f"Error inserting application: {e}")

    await message.answer("Salom! 👋", reply_markup=await admin_kb(message.from_user.id))
