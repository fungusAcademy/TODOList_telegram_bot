from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.task_service import TaskService
from dependency_injector.wiring import Provide, inject

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

• Напиши /add + текст задачи чтобы добавить новую задачу
• Напиши /list чтобы посмотреть все задачи
• Напиши /del чтобы удалить все задачи
    """

# keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="Добавить задачу"), KeyboardButton(text="Список задач")], 
#         [KeyboardButton(text="Очистить список задач"), KeyboardButton(text="Помощь")]
#     ],
#     resize_keyboard=True
# )

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    """/start command handler"""
    # await message.answer(WELCOME_TEXT, reply_markup=keyboard)
    await message.answer(WELCOME_TEXT)

@router.message(Command('help'))
@router.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    """/help command handler"""
    await message.answer(HELP_TEXT)

@router.message(Command('add'))
@inject
# @router.message(lambda message: message.text == "Добавить задачу")
async def add_task(
    message: types.Message,
    task_service: TaskService = Provide['task_service']
    ):
    """/add command handler"""
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

async def add_task_for_test(
    message: types.Message,
    task_service: TaskService
):
    """FOR TESTS without DI
    /add command handler """
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
async def list_tasks(
    message: types.Message,
    task_service: TaskService = Provide['task_service']
    ):
    """/list command handler"""
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


async def list_tasks_for_test(
    message: types.Message,
    task_service: TaskService
):
    """FOR TESTS without DI
    /list command handler """
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

@router.message(Command('del'))
@inject
async def delete_task(
    message: types.Message,
    task_service: TaskService = Provide['task_service']
):
    if message.from_user is not None:
        user_id = message.from_user.id
    else:
        raise TypeError('user id is None')
    
    if message.text is None:
        raise TypeError('Task id is None')
    
    try:
        task_id = int(message.text.replace('/del', '').strip())
        result = await task_service.delete_task(user_id, task_id)

        if result:
            await message.answer(f"✅ Задача #{task_id} удалена из базы")
        else:
            await message.answer(f"❌ Задача #{task_id} отсутствует в базе")
    except ValueError:
        await message.answer(f"❌ Введите номер задачи для удаления!")
        return
    except Exception as e:
        await message.answer("❌ Ошибка при получении задач из базы")
        print(f"Ошибка: {e}")

async def delete_task_for_test(
    message: types.Message,
    task_service: TaskService
):
    if message.from_user is not None:
        user_id = message.from_user.id
    else:
        raise TypeError('user id is None')
    
    if message.text is None:
        raise TypeError('Task id is None')
    
    try:
        task_id = int(message.text.replace('/del', '').strip())
        result = await task_service.delete_task(user_id, task_id)

        if result:
            await message.answer(f"✅ Задача #{task_id} удалена из базы")
        else:
            await message.answer(f"❌ Задача #{task_id} отсутствует в базе")
    except ValueError:
        await message.answer(f"❌ Введите номер задачи для удаления!")
        return
    except Exception as e:
        await message.answer("❌ Ошибка при получении задач из базы")
        print(f"Ошибка: {e}")