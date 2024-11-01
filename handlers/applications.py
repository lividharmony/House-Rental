from aiogram import types, Router, Dispatcher, Bot
from aiogram.filters import CommandStart, state

router = Router()


@router.message(CommandStart())
async def apply_for_housing(message: types.Message, dispatcher: Dispatcher, bot: Bot):
    housing_id = 1
    user_id = message.from_user.id
    pool = dispatcher['db']
    async with pool.acquire() as connection:
        result = await connection.fetchrow("SELECT * FROM users WHERE user_id = $1", str(user_id))

        if result is None:
            # registerni integratsiya qilish
            await message.answer('a')
            # await start_registration(message, state, bot)

    # async with pool.acquire() as connection:
    #     await connection.execute(
    #         "INSERT INTO applications (user_id, housing_id) VALUES ($1, $2)", user_id, housing_id
    #     )
    #
    # await bot.send_message(
    #     ADMINS,
    #     f"Yangi ariza tushdi!\nFoydalanuvchi ID: {user_id}, Uy-joy ID: {housing_id}"
    # )
    await message.answer("Arizangiz qabul qilindi!")
