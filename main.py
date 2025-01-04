import asyncio    # импортим нужные библиотеки
import logging
import sys
import os

from aiogram import Bot, Dispatcher    # импортим нужное из аиограма
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv, find_dotenv

import handler    # импортим файл обработки сообщений

load_dotenv(find_dotenv())    # подгружаем файлик .env


# ну всё дальше - это дефолтная конструкция из документации аиограма

async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    dp.include_routers(handler.router)  # тут добавляем роутер
    await dp.start_polling(bot)    # стартуем бота!


if __name__ == "__main__":
    BOT_TOKEN = os.getenv("BOT_TOKEN")  # получаем токен бота из переменной окружения в файле .env
    if BOT_TOKEN is None:    # проверяем наличие токена там
        raise ValueError("BOT_TOKEN is not set")

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())    # запускаем основную функцию бота