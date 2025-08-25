import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.commands import router
from aiogram.fsm.storage.memory import MemoryStorage
from repositories.task_repository import InMemoryTaskRepository
from services.task_service import TaskService 

async def main():
    if BOT_TOKEN is not None:
        bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    task_repository = InMemoryTaskRepository()
    task_service = TaskService(task_repository)
    dp["task_service"] = task_service

    # Передаем сервис в хендлеры
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())