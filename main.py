# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers.commands import router
from database import init_db

async def main():
    await init_db()
    
    if BOT_TOKEN is not None:
        bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    print("Бот запущен с PostgreSQL!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())