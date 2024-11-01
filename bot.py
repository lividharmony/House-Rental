import asyncio
import logging
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.applications import router

from database import create_db_pool, initialize_database
import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
dp.include_router(router)


async def on_startup():
    dp['db'] = await create_db_pool()
    await initialize_database(dp['db'])


async def on_shutdown():
    await dp['db'].close()


def register_handlers():
    dp.include_router(router)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
