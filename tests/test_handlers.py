import pytest
from unittest.mock import AsyncMock
from handlers.commands import add_task_for_test, list_tasks_for_test, delete_task_for_test

@pytest.mark.asyncio
async def test_add_task_handler_success(mock_message, mock_task_service):
    """Test for adding task successfully"""
    mock_message.text = "/add Test task"

    await add_task_for_test(mock_message, mock_task_service)
    
    # Check if service -> create_task called once
    mock_task_service.create_task.assert_called_once_with(12345, "Test task")
    
    # Check if bot answer on adding task is success
    mock_message.answer.assert_called_once_with("✅ Задача #1 добавлена в базу: Test task")

@pytest.mark.asyncio
async def test_add_task_handler_empty_text(mock_message, mock_task_service):
    """Test for adding empty task text"""
    mock_message.text = "/add"
    
    await add_task_for_test(mock_message, mock_task_service)
    
    # Service should not be called
    mock_task_service.create_task.assert_not_called()
    
    # Check if expected answer is empty input error message
    mock_message.answer.assert_called_once_with("❌ Введите задачу после команды /add")

@pytest.mark.asyncio
async def test_add_task_handler_service_error(mock_message, mock_task_service):
    """Test for service error behaviour"""
    mock_message.text = "/add Test task"
    # Simulate DB access error for service
    mock_task_service.create_task.side_effect = Exception("DB error")
    
    await add_task_for_test(mock_message, mock_task_service)
    
    # Service should not be called
    mock_task_service.create_task.assert_called_once_with(12345, "Test task")
    
    # Check if expected answer is DB error message
    mock_message.answer.assert_called_once_with("❌ Ошибка при добавлении в базу")

@pytest.mark.asyncio
async def test_list_tasks_handler_success(mock_message, mock_task_service):
    """Test for getting task list successfully"""
    mock_message.text = "/list"

    from models.task import Task
    
    # Create mock tasks
    mock_tasks = [
        Task(id=1, user_id=12345, task_text="Test task 1"),
        Task(id=2, user_id=12345, task_text="Test task 2")
    ]
    
    mock_task_service.get_user_tasks.return_value = mock_tasks
    
    await list_tasks_for_test(mock_message, mock_task_service)
    
    # Check if service is called
    mock_task_service.get_user_tasks.assert_called_once_with(12345)
    
    # Check if bot answer is correct
    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "📋 Задачи из базы данных:" in call_args
    assert "Test task 1" in call_args
    assert "Test task 2" in call_args

@pytest.mark.asyncio
async def test_list_tasks_handler_empty(mock_message, mock_task_service):
    """Test for getting empty task list"""
    mock_message.text = "/list"
    mock_task_service.get_user_tasks.return_value = []
    
    await list_tasks_for_test(mock_message, mock_task_service)
    
    mock_task_service.get_user_tasks.assert_called_once_with(12345)
    mock_message.answer.assert_called_once_with("📭 В базе нет задач")

@pytest.mark.asyncio
async def test_list_tasks_handler_service_error(mock_message, mock_task_service):
    """Test for service error behaviour"""
    mock_message.text = "/list"
    mock_task_service.get_user_tasks.side_effect = Exception("DB error")
    
    from handlers.commands import list_tasks_for_test
    await list_tasks_for_test(mock_message, mock_task_service)
    
    mock_task_service.get_user_tasks.assert_called_once_with(12345)
    mock_message.answer.assert_called_once_with("❌ Ошибка при получении задач из базы")

@pytest.mark.asyncio
async def test_delete_task_handler_success(mock_message, mock_task_service):
    """Test for deleting task successfully"""
    mock_message.text = "/del 1"
    mock_task_service.delete_task.return_value = True
    
    await delete_task_for_test(mock_message, mock_task_service)
    
    # Check if service is called
    mock_task_service.delete_task.assert_called_once_with(12345, 1)
    
    # Check bot answer
    mock_message.answer.assert_called_once_with("✅ Задача #1 удалена из базы")

@pytest.mark.asyncio
async def test_delete_task_handler_not_found(mock_message, mock_task_service):
    """Test for deleting task not present in DB"""
    mock_message.text = "/del 999"
    mock_task_service.delete_task.return_value = False
    
    await delete_task_for_test(mock_message, mock_task_service)
    
    mock_task_service.delete_task.assert_called_once_with(12345, 999)
    mock_message.answer.assert_called_once_with("❌ Задача #999 отсутствует в базе")

@pytest.mark.asyncio
async def test_delete_task_handler_no_id(mock_message, mock_task_service):
    """Test for deleting withoud stating ID"""
    mock_message.text = "/del"
    
    await delete_task_for_test(mock_message, mock_task_service)
    
    # Service should NOT be called
    mock_task_service.delete_task.assert_not_called()
    
    # Check for right answer
    mock_message.answer.assert_called_once_with("❌ Введите номер задачи для удаления!")

@pytest.mark.asyncio
async def test_delete_task_handler_invalid_id(mock_message, mock_task_service):
    """Test for deleting with invalid ID"""
    mock_message.text = "/del invalid"
    
    await delete_task_for_test(mock_message, mock_task_service)
    
    # Service should NOT be called
    mock_task_service.delete_task.assert_not_called()
    
    # Check for right error answer
    mock_message.answer.assert_called_once_with("❌ Введите номер задачи для удаления!")

@pytest.mark.asyncio
async def test_delete_task_handler_service_error(mock_message, mock_task_service):
    """Test for service error behaviour"""
    mock_message.text = "/del 1"
    mock_task_service.delete_task.side_effect = Exception("DB error")
    
    await delete_task_for_test(mock_message, mock_task_service)
    
    mock_task_service.delete_task.assert_called_once_with(12345, 1)
    mock_message.answer.assert_called_once_with("❌ Ошибка при получении задач из базы")