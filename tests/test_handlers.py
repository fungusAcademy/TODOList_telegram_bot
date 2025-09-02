import pytest
from unittest.mock import AsyncMock, patch
from handlers.commands import add_task, list_tasks

@pytest.mark.asyncio
async def test_add_task_handler_success(mock_message):
    """Тест успешного добавления задачи"""
    with patch('handlers.commands.add_task') as mock_add:
        mock_add.return_value = 1
        
        await add_task(mock_message)
        
        # Проверяем что функция вызвалась
        mock_add.assert_called_once_with(12345, "Test task")
        
        # Проверяем что бот ответил
        mock_message.answer.assert_called_once_with("✅ Задача #1 добавлена в базу: Test task")

@pytest.mark.asyncio
async def test_add_task_handler_empty_text():
    """Тест добавления пустой задачи"""
    message = AsyncMock()
    message.from_user.id = 12345
    message.text = "/add"
    message.replace.return_value = ""
    
    await add_task(message)
    
    # Проверяем что бот ответил ошибкой
    message.answer.assert_called_once_with("❌ Введите задачу после команды /add")

@pytest.mark.asyncio
async def test_list_tasks_handler_empty():
    """Тест пустого списка задач"""
    message = AsyncMock()
    message.from_user.id = 12345
    
    with patch('handlers.commands.list_tasks') as mock_get:
        mock_get.return_value = []
        
        await list_tasks(message)
        
        # Проверяем ответ
        message.answer.assert_called_once_with("📭 В базе нет задач")