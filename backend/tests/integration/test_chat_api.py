import pytest
from httpx import AsyncClient
from src.main import app
from src.models.user import User
from src.db import async_session_factory
from sqlmodel import select

@pytest.mark.asyncio
async def test_chat_endpoint_persistence():
    """Test that messages are persisted in the database."""
    user_id = 1
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            f"/api/chat/{user_id}/chat",
            json={"message": "Hello agent"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    
    # Verify in DB
    async with async_session_factory() as session:
        from src.models.message import Message
        statement = select(Message).where(Message.user_id == user_id)
        result = await session.execute(statement)
        messages = result.scalars().all()
        
        # Should have at least 2 messages (user + assistant)
        assert len(messages) >= 2
        assert any(m.role == "user" and m.content == "Hello agent" for m in messages)
        assert any(m.role == "assistant" for m in messages)
