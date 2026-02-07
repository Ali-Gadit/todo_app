import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.agent.tools import (
    add_task_impl, 
    list_tasks_impl, 
    complete_task_impl, 
    delete_task_impl, 
    update_task_impl
)
from src.models.task import Task, TaskStatus

@pytest.mark.asyncio
async def test_add_task():
    # Mock the session
    mock_session = MagicMock() # Use MagicMock for sync methods
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock() # commit is async in AsyncSession
    mock_session.refresh = AsyncMock() # refresh is async in AsyncSession
    
    # Mock the returned task object to have an ID
    def add_side_effect(instance): 
        instance.id = 123
    
    mock_session.add.side_effect = add_side_effect
    
    # Setup mock for async context manager
    mock_factory = MagicMock()
    mock_factory.__aenter__.return_value = mock_session
    mock_factory.__aexit__.return_value = AsyncMock() # __aexit__ must return an awaitable
    
    # Patch the session factory in tools
    with patch("src.agent.tools.async_session_factory", return_value=mock_factory):
        # Call the tool
        result = await add_task_impl(user_id="1", title="Buy milk", description="Low fat")
        
        # Verify result
        assert result["status"] == "created"
        assert result["title"] == "Buy milk"
        assert result["task_id"] == 123
        
        # Verify session usage
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_add_task_invalid_user_id():
    result = await add_task_impl(user_id="abc", title="Test")
    assert result["status"] == "error"

@pytest.mark.asyncio
async def test_list_tasks():
    task1 = Task(id=1, user_id=1, title="Task 1", status=TaskStatus.PENDING)
    
    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [task1]
    mock_session.execute.return_value = mock_result
    
    mock_factory = MagicMock()
    mock_factory.__aenter__.return_value = mock_session
    mock_factory.__aexit__.return_value = AsyncMock()
    
    with patch("src.agent.tools.async_session_factory", return_value=mock_factory):
        result = await list_tasks_impl(user_id="1", status="all")
        assert len(result) == 1
        assert result[0]["title"] == "Task 1"

@pytest.mark.asyncio
async def test_complete_task():
    task = Task(id=1, user_id=1, title="Task 1", status=TaskStatus.PENDING)
    
    mock_session = MagicMock()
    mock_session.get = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    mock_session.get.return_value = task
    
    mock_factory = MagicMock()
    mock_factory.__aenter__.return_value = mock_session
    mock_factory.__aexit__.return_value = AsyncMock()
    
    with patch("src.agent.tools.async_session_factory", return_value=mock_factory):
        result = await complete_task_impl(user_id="1", task_id=1)
        assert result["status"] == "completed"
        assert task.status == TaskStatus.COMPLETED

@pytest.mark.asyncio
async def test_delete_task():
    task = Task(id=1, user_id=1, title="Task 1")
    
    mock_session = MagicMock()
    mock_session.get = AsyncMock()
    mock_session.delete = AsyncMock() # delete is usually async in AsyncSession or sync depending on impl
    mock_session.commit = AsyncMock()
    
    # In SQLModel/SQLAlchemy AsyncSession, delete is sync but commit is async
    # Let's make it sync to be safe if it's sync
    mock_session.delete = MagicMock()
    
    mock_session.get.return_value = task
    
    mock_factory = MagicMock()
    mock_factory.__aenter__.return_value = mock_session
    mock_factory.__aexit__.return_value = AsyncMock()
    
    with patch("src.agent.tools.async_session_factory", return_value=mock_factory):
        result = await delete_task_impl(user_id="1", task_id=1)
        assert result["status"] == "deleted"
        mock_session.delete.assert_called_once_with(task)

@pytest.mark.asyncio
async def test_update_task():
    task = Task(id=1, user_id=1, title="Old Title")
    
    mock_session = MagicMock()
    mock_session.get = AsyncMock()
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    
    mock_session.get.return_value = task
    
    mock_factory = MagicMock()
    mock_factory.__aenter__.return_value = mock_session
    mock_factory.__aexit__.return_value = AsyncMock()
    
    with patch("src.agent.tools.async_session_factory", return_value=mock_factory):
        result = await update_task_impl(user_id="1", task_id=1, title="New Title")
        assert result["status"] == "updated"
        assert task.title == "New Title"