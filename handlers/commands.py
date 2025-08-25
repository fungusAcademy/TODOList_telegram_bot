from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from services.task_service import TaskService
from handlers.inline_kbs import ease_link_kb

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

# Клавиатура
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить задачу"), KeyboardButton(text="Список задач")], 
        [KeyboardButton(text="Очистить список задач"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)


# Команда /start
@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(WELCOME_TEXT, reply_markup=keyboard)
    await message.answer("Мои контакты: ", reply_markup=ease_link_kb())

# Команда /help
@router.message(Command('help'))
@router.message(lambda message: message.text == "Помощь")
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

# команда /add
@router.message(Command('add'))
# @router.message(lambda message: message.text == "Добавить задачу")
async def add_task(message: types.Message, task_service: TaskService):
    if message.text is not None:
        task_text = message.text.replace('/add', '').strip()
        # Добавить вызов cmd_help в случае если нет текста от пользователя
        if  not len(task_text): return
        if message.from_user is not None:
            task = await task_service.create_task(task_text, message.from_user.id)
            await message.answer(f"✅ Задача добавлена: {task.text}")
    # if message.from_user is not None:
    #     user_id = message.from_user.id
    # else:
    #     pass
    # if user_id not in user_tasks:
    #     user_tasks[user_id] = []
    
    # # Просим ввести задачу
    # await message.answer("📝 Введите задачу:")

# Список задач
@router.message(Command('list'))
# @router.message(lambda message: message.text == "Список задач")
async def list_tasks(message: types.Message, task_service: TaskService):
    if message.from_user is not None:
        tasks = await task_service.get_user_tasks(message.from_user.id)
        if not tasks:
            await message.answer("📝 Список задач пуст")
            return
        # ------ Следует перенести в модуль View
        tasks_text = "\n".join([f"{'✅' if task.is_done else '⏳'} {task.id}: {task.text}" for task in tasks])
        # ------
        await message.answer(f"📋 Список задач: \n{tasks_text}")
    # if message.from_user is not None:
    #     user_id = message.from_user.id
    # else: 
    #     pass
    # if user_id not in user_tasks or not user_tasks[user_id]:
    #     await message.answer("📭 Список задач пуст")
    #     return
    # tasks_list = "\n".join([f"• {task}" for task in user_tasks[user_id]])
    # await message.answer(f"📋 Ваши задачи:\n{tasks_list}")

# Удаление задачи
@router.message(Command('del'))
# @router.message(lambda message: message.text == "Очистить список задач")
async def del_tasks(message: types.Message, task_service: TaskService):
    # Добавить обработку ввода, если ввели не число или неверное число
    if message.text is not None:
        try:
            id = int(message.text.replace('/del', '').strip())
        except:
            await message.answer("Пожалуйста, введите номер заметки, которую нужно удалить!")
            return
        await task_service.delete_task(id)
        await message.answer(f"Задача №{id} успешно удалена!")

    # --------------------------------
    # if message.from_user is not None:
    #     user_id = message.from_user.id
    # else:
    #     pass
    # if user_id not in user_tasks or not user_tasks[user_id]:
    #     await message.answer("📭 Список задач пуст")
    #     return
    # user_tasks.clear()
    # await message.answer("📭 Список задач очищен")

# @router.message(lambda message: message.text == "Инлайн")
# async def get_inline_btn_link(message: types.Message): 
#     await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=ease_link_kb())

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