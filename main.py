import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.commands import router

if BOT_TOKEN is not None:
    bot = Bot(token=BOT_TOKEN)
else:
    pass 
# Add error handling
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())