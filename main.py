# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from di.containers import Container
from handlers.commands import router
from config import BOT_TOKEN, DATABASE_DSN

async def main():
    # container DI setup
    container = Container()
    container.config.database.dsn.from_value(DATABASE_DSN)

    # Bot initialization
    if BOT_TOKEN: bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Dependency injection
    container.wire(modules=["handlers.commands"])
    # container.wire(modules=[handlers.commands])


    # router connect
    dp.include_router(router)

    # Start
    print("Bot is running!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())