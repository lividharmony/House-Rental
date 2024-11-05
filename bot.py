import asyncio
import logging
import sys
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.applications import router as applications_router
from handlers.register import router as register_router
from handlers.admin import router as admin_router
from handlers.callbackquery import router as callback_router
from handlers.Listings import router as listings_router
from handlers.search import router as search_router

from database import create_db_pool, initialize_database
import config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
dp.include_routers(applications_router,
                   register_router,
                   admin_router,
                   callback_router,
                   listings_router,
                   search_router
                   )


async def on_startup():
    dp['db'] = await create_db_pool()
    await initialize_database(dp['db'])


async def on_shutdown():
    await dp['db'].close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.run_polling(bot)
