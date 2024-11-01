from aiogram import types, Router
from bot import dp, bot
import executor
from config import ADMINS

from aiogram.filters import Command

router = Router()


async def notify_users_about_new_housing(description):
    pool = dp['db']
    async with pool.acquire() as connection:
        users = await connection.fetch("SELECT id FROM users WHERE user_type = 'student'")

    for user in users:
        await bot.send_message(user['id'], f"Yangi uy-joy qo'shildi: {description}")


@router.message(Command("add_housing"), user_id=ADMINS)
async def add_housing_and_notify(message: types.Message):
    description = "Toshkentdagi yangi uy-joy"
    await notify_users_about_new_housing(description)
    await message.answer("Uy-joy qo'shildi va barcha foydalanuvchilarga xabar yuborildi!")
