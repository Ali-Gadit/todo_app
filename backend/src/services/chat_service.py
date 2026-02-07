from typing import List, Optional, Dict, Any, AsyncIterator
import json
from sqlmodel import select, Session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from chatkit.store import Store, NotFoundError
from chatkit.types import (
    ThreadMetadata, 
    ThreadItem, 
    UserMessageItem, 
    AssistantMessageItem, 
    AssistantMessageContent, 
    Page, 
    UserMessageContent,
    UserMessageTextContent,
    Attachment,
    InferenceOptions,
    ClientToolCallItem
)
from chatkit.server import ThreadStreamEvent, ThreadItemDoneEvent

from ..models.conversation import Conversation
from ..models.message import Message
from ..db import async_session_factory

class SQLModelChatStore(Store[dict]):
    """SQLModel implementation of the ChatKit Store interface."""

    async def load_thread(self, thread_id: str, context: dict) -> ThreadMetadata:
        user_id = context.get("user_id")
        if not thread_id:
             raise NotFoundError(f"Invalid thread ID {thread_id}")
             
        async with async_session_factory() as session:
            statement = select(Conversation).where(
                Conversation.id == thread_id,
                Conversation.user_id == user_id
            )
            result = await session.execute(statement)
            conv = result.scalars().first()
            if not conv:
                raise NotFoundError(f"Thread {thread_id} not found")
            return ThreadMetadata(id=str(conv.id), created_at=conv.created_at)

    async def save_thread(self, thread: ThreadMetadata, context: dict) -> None:
        user_id = context.get("user_id")
        async with async_session_factory() as session:
            # Check if exists
            statement = select(Conversation).where(Conversation.id == thread.id)
            result = await session.execute(statement)
            conv = result.scalars().first()
            if not conv:
                conv = Conversation(id=thread.id, user_id=user_id, created_at=thread.created_at)
                session.add(conv)
            else:
                conv.updated_at = datetime.utcnow()
            await session.commit()

    async def load_threads(
        self, limit: int, after: Optional[str], order: str, context: dict
    ) -> Page[ThreadMetadata]:
        user_id = context.get("user_id")
        async with async_session_factory() as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            
            if order == "desc":
                statement = statement.order_by(Conversation.created_at.desc())
            else:
                statement = statement.order_by(Conversation.created_at.asc())
            
            if after:
                if order == "desc":
                    statement = statement.where(Conversation.id < after)
                else:
                    statement = statement.where(Conversation.id > after)
            
            statement = statement.limit(limit)
            result = await session.execute(statement)
            conversations = result.scalars().all()
            
            items = [ThreadMetadata(id=str(c.id), created_at=c.created_at) for c in conversations]
            has_more = len(items) == limit
            next_after = items[-1].id if items else None
            return Page(data=items, has_more=has_more, after=next_after)

    async def load_thread_items(
        self, thread_id: str, after: Optional[str], limit: int, order: str, context: dict
    ) -> Page[ThreadItem]:
        async with async_session_factory() as session:
            statement = select(Message).where(Message.conversation_id == thread_id)
            
            if order == "desc":
                statement = statement.order_by(Message.created_at.desc())
            else:
                statement = statement.order_by(Message.created_at.asc())
            
            if after:
                if order == "desc":
                    statement = statement.where(Message.id < after)
                else:
                    statement = statement.where(Message.id > after)
            
            statement = statement.limit(limit)
            result = await session.execute(statement)
            messages = result.scalars().all()
            
            items = []
            for m in messages:
                if m.role == "user":
                    items.append(UserMessageItem(
                        id=str(m.id),
                        thread_id=str(m.conversation_id),
                        created_at=m.created_at,
                        content=[UserMessageTextContent(text=m.content)],
                        inference_options=InferenceOptions()
                    ))
                elif m.role == "tool_call":
                    try:
                        data = json.loads(m.content)
                        # Ensure created_at is datetime
                        if "created_at" in data and isinstance(data["created_at"], str):
                            data["created_at"] = datetime.fromisoformat(data["created_at"])
                        
                        # Fix for Groq/OpenAI: ensure output is not None
                        if data.get("output") is None:
                            data["output"] = ""
                        elif not isinstance(data["output"], str):
                            # If it's a dict/list, serialize it to string as chatkit expects
                            data["output"] = json.dumps(data["output"])
                            
                        items.append(ClientToolCallItem.model_validate(data))
                    except Exception as e:
                        print(f"Error loading tool call {m.id}: {e}")
                        continue
                else:
                    items.append(AssistantMessageItem(
                        id=str(m.id),
                        thread_id=str(m.conversation_id),
                        created_at=m.created_at,
                        content=[AssistantMessageContent(text=m.content)]
                    ))
            
            has_more = len(items) == limit
            next_after = items[-1].id if items else None
            return Page(data=items, has_more=has_more, after=next_after)

    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: dict) -> None:
        user_id = context.get("user_id")
        
        # Handle __fake_id__ placeholder from agents library
        if item.id == "__fake_id__":
            item.id = self.generate_item_id(item.type, None, context)

        async with async_session_factory() as session:
            # Check if exists to avoid IntegrityError (duplicate key)
            statement = select(Message).where(Message.id == item.id)
            result = await session.execute(statement)
            if result.scalars().first():
                # Item already exists, redirect to save_item for update
                await self.save_item(thread_id, item, context)
                return

            content = ""
            role = "assistant"
            
            if isinstance(item, UserMessageItem):
                role = "user"
                if hasattr(item, "content"):
                    for part in item.content:
                        if hasattr(part, "text"):
                            content += part.text
            elif isinstance(item, ClientToolCallItem):
                role = "tool_call"
                # Ensure output is a string before serializing, 
                # because Groq/OpenAI require a string content for tool messages
                if item.output is None:
                    item.output = ""
                elif not isinstance(item.output, str):
                    item.output = json.dumps(item.output)
                
                # Serialize the whole item to JSON
                content = item.model_dump_json()
            else:
                # Assistant message
                if hasattr(item, "content"):
                    for part in item.content:
                        if hasattr(part, "text"):
                            content += part.text
            
            new_msg = Message(
                id=item.id,
                conversation_id=thread_id,
                user_id=user_id,
                role=role,
                content=content,
                created_at=item.created_at
            )
            session.add(new_msg)
            await session.commit()

    async def save_item(self, thread_id: str, item: ThreadItem, context: dict) -> None:
        user_id = context.get("user_id")

        # Handle __fake_id__ placeholder from agents library
        if item.id == "__fake_id__":
            item.id = self.generate_item_id(item.type, None, context)

        async with async_session_factory() as session:
            statement = select(Message).where(Message.id == item.id)
            result = await session.execute(statement)
            existing = result.scalars().first()
            if existing:
                if isinstance(item, ClientToolCallItem):
                    if item.output is None:
                        item.output = ""
                    elif not isinstance(item.output, str):
                        item.output = json.dumps(item.output)
                    
                    existing.content = item.model_dump_json()
                    # ensure role is correct just in case
                    existing.role = "tool_call"
                else:
                    content = ""
                    if hasattr(item, "content"):
                        for part in item.content:
                            if hasattr(part, "text"):
                                content += part.text
                    existing.content = content
                
                session.add(existing)
                await session.commit()
                return
            
            await self.add_thread_item(thread_id, item, context)

    async def load_item(self, thread_id: str, item_id: str, context: dict) -> ThreadItem:
        async with async_session_factory() as session:
            statement = select(Message).where(Message.id == item_id)
            result = await session.execute(statement)
            m = result.scalars().first()
            if not m:
                raise NotFoundError(f"Item {item_id} not found")
            
            if m.role == "user":
                return UserMessageItem(
                    id=str(m.id),
                    thread_id=str(m.conversation_id),
                    created_at=m.created_at,
                    content=[UserMessageTextContent(text=m.content)],
                    inference_options=InferenceOptions()
                )
            elif m.role == "tool_call":
                data = json.loads(m.content)
                if "created_at" in data and isinstance(data["created_at"], str):
                    data["created_at"] = datetime.fromisoformat(data["created_at"])
                
                # Fix for Groq/OpenAI: ensure output is not None
                if data.get("output") is None:
                    data["output"] = ""
                elif not isinstance(data["output"], str):
                    data["output"] = json.dumps(data["output"])

                return ClientToolCallItem.model_validate(data)
            else:
                return AssistantMessageItem(
                    id=str(m.id),
                    thread_id=str(m.conversation_id),
                    created_at=m.created_at,
                    content=[AssistantMessageContent(text=m.content)]
                )

    async def delete_thread(self, thread_id: str, context: dict) -> None:
        async with async_session_factory() as session:
            statement = select(Conversation).where(Conversation.id == thread_id)
            result = await session.execute(statement)
            conv = result.scalars().first()
            if conv:
                await session.delete(conv)
                await session.commit()

    async def delete_thread_item(self, thread_id: str, item_id: str, context: dict) -> None:
        async with async_session_factory() as session:
            statement = select(Message).where(Message.id == item_id)
            result = await session.execute(statement)
            msg = result.scalars().first()
            if msg:
                await session.delete(msg)
                await session.commit()

    async def save_attachment(self, attachment: Attachment, context: dict) -> None:
        pass

    async def load_attachment(self, attachment_id: str, context: dict) -> Attachment:
        raise NotFoundError("Attachments not implemented")

    async def delete_attachment(self, attachment_id: str, context: dict) -> None:
        pass

    def generate_thread_id(self, context: dict) -> str:
        import random
        return str(random.randint(1000, 999999))

    def generate_item_id(self, type: str, thread: ThreadMetadata, context: dict) -> str:
        import random
        return str(int(datetime.utcnow().timestamp()) * 1000 + random.randint(0, 999))