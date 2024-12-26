# -*- coding: utf-8 -*-
import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_handlers
from logger import setup_logging

logger = setup_logging()

load_dotenv(".env.local")
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def start_polling():
    try:
        print("Осуществлён запуск бота")
        logger.info("Осуществлён запуск бота")
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling был отменен.")
        logger.warning("Polling был отменен.")
    except KeyboardInterrupt:
        print("Бот остановлен.")
        logger.warning("Бот остановлен.")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(start_polling())
