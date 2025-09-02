from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.task_service import TaskService
from dependency_injector.wiring import Provide, inject
# from db_operations import add_task_to_db, get_user_tasks_from_db

router = Router()

WELCOME_TEXT = """
🤖 Привет! Я бот-помощник для учета задач.

Доступные команды:
/start - начать работу
/add - добавить задачу
/list - список задач
/del - удалить задачу
/help - помощь

Или используй кнопки ниже!
    """
HELP_TEXT = """
📋 Как пользоваться ботом:

• Нажми "Добавить задачу" или напиши /add + текст задачи чтобы добавить новую задачу
• Нажми "Список задач" или напиши /list чтобы посмотреть все задачи
• Нажми "удалить" или напиши /del чтобы удалить все задачи
• Задачи сохраняются в памяти (после перезапуска бота пропадут)
    """

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить задачу"), KeyboardButton(text="Список задач")], 
        [KeyboardButton(text="Очистить список задач"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    # await message.answer(WELCOME_TEXT, reply_markup=keyboard)
    await message.answer(WELCOME_TEXT)

@router.message(Command('help'))
@router.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

@router.message(Command('add'))
@inject
# @router.message(lambda message: message.text == "Добавить задачу")
async def add_task(
    message: types.Message,
    task_service: TaskService = Provide['task_service']
    ):
    if message.from_user is not None:
        user_id = message.from_user.id
    else:
        raise TypeError('user id is None')
    
    if message.text is not None:
        task_text = message.text.replace('/add', '').strip()
    else:
        raise TypeError('task text is None')
        
    if not task_text:
        await message.answer("❌ Введите задачу после команды /add")
        return

    try:
        task_id = await task_service.create_task(user_id, task_text)
        await message.answer(f"✅ Задача #{task_id} добавлена в базу: {task_text}")
    except Exception as e:
        await message.answer("❌ Ошибка при добавлении в базу")
        print(f"Ошибка: {e}")

@router.message(Command('list'))
@inject
# @router.message(lambda message: message.text == "Список задач")
# Tasks now are printed in reverse order -_-
async def list_tasks(
    message: types.Message,
    task_service: TaskService = Provide['task_service']
    ):
    if message.from_user is not None:
        user_id = message.from_user.id
    else:
        raise TypeError('user id is None')
    
    try:
        tasks = await task_service.get_user_tasks(user_id)
        
        if not tasks:
            await message.answer("📭 В базе нет задач")
            return
        
        tasks_list = "\n".join([f"• {task.task_text} (ID: {task.id})" for task in tasks])
        await message.answer(f"📋 Задачи из базы данных:\n{tasks_list}")
    except Exception as e:
        await message.answer("❌ Ошибка при получении задач из базы")
        print(f"Ошибка: {e}")

# @router.message(Command('del'))
# # @router.message(lambda message: message.text == "Очистить список задач")
# async def del_tasks(message: types.Message, task_service: TaskService):
#     # Добавить обработку ввода, если ввели не число или неверное число
#     if message.text is not None:
#         try:
#             id = int(message.text.replace('/del', '').strip())
#         except:
#             await message.answer("Пожалуйста, введите номер заметки, которую нужно удалить!")
#             return
#         await task_service.delete_task(id)
#         await message.answer(f"Задача №{id} успешно удалена!")

# # Обработка ввода задачи
# @router.message(lambda message: message.text and message.text not in ["Добавить задачу", "Список задач", "Очистить список задач", "Помощь"])
# async def process_task_input(message: types.Message):
#     if message.from_user is not None:
#         user_id = message.from_user.id
#     else:
#         pass
#     task_text = message.text
    
#     if user_id not in user_tasks:
#         user_tasks[user_id] = []
    
#     user_tasks[user_id].append(task_text)
#     await message.answer(f"✅ Задача добавлена: {task_text}")