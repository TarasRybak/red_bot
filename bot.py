import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from handlers import common, flashcards


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Если не указать storage, то по умолчанию всё равно будет MemoryStorage
    # Но явное лучше неявного =]
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    dp.include_routers(common.router, flashcards.router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
