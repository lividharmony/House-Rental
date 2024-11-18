from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("/start"))
async def start_command(message: types.Message):
    await message.reply("Salom 👋! Botga xush kelibsiz")


@router.message(Command("/help"))
async def help_command(message: types.Message):
    await message.reply("Yordam uchun:\n"
                        "/start - Botni boshlash\n"
                        "/help - Yordam olish")
