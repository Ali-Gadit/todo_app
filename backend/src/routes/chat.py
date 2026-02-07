from typing import AsyncIterator, List, Any, Optional
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from chatkit.server import ChatKitServer, ThreadMetadata, UserMessageItem, ThreadStreamEvent, ThreadItemDoneEvent, StreamingResult
from chatkit.agents import AgentContext, simple_to_agent_input, stream_agent_response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import secrets
import traceback

from ..services.chat_service import SQLModelChatStore
from ..agent.agent import todo_agent, run_config
from ..db import get_session

router = APIRouter()
store = SQLModelChatStore()

class AgentChatKitServer(ChatKitServer[dict]):
    async def respond(
        self,
        thread: ThreadMetadata,
        input_user_message: UserMessageItem | None,
        context: dict,
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Stream responses from the Todo Agent."""
        try:
            user_id = context.get("user_id")
            print(f"DEBUG: respond() triggered for user {user_id}, thread {thread.id}")
            
            # Load thread items
            items_page = await self.store.load_thread_items(
                thread.id, after=None, limit=20, order="asc", context=context
            )
            
            # Convert to agent input
            input_items = await simple_to_agent_input(items_page.data)
            
            # Prepend system context about user_id
            input_items.insert(0, {"role": "system", "content": f"The current user_id is {user_id}. You are helping this user manage their tasks."})

            # Create agent context
            agent_context = AgentContext(
                thread=thread,
                store=self.store,
                request_context=context
            )

            # Run agent streamed
            from agents import Runner
            result = Runner.run_streamed(todo_agent, input_items, context=agent_context, run_config=run_config)

            async for event in stream_agent_response(agent_context, result):
                yield event
        except Exception as e:
            print(f"ERROR in AgentChatKitServer.respond: {str(e)}")
            traceback.print_exc()
            raise

server = AgentChatKitServer(store=store)

@router.get("/session")
async def create_session():
    """Create a new ChatKit session token."""
    return {"client_secret": secrets.token_urlsafe(32), "expires_in": 3600}

@router.post("/{user_id}/chat")
async def chatkit_endpoint(
    user_id: int,
    request: Request
):
    """Unified endpoint for ChatKit communication."""
    try:
        print(f"DEBUG: ChatKit request for user {user_id}")
        context = {"user_id": user_id}
        body = await request.body()
        print(f"DEBUG: Body length: {len(body)}")
        
        # Process the request through the ChatKit server
        result = await server.process(body, context)
        
        if isinstance(result, StreamingResult):
            async def stream_generator():
                try:
                    async for chunk in result:
                        yield chunk
                except Exception as stream_err:
                    print(f"ERROR in stream_generator: {str(stream_err)}")
                    traceback.print_exc()
            
            return StreamingResponse(
                stream_generator(), 
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )
        
        return Response(content=result.json, media_type="application/json")
    except Exception as e:
        print(f"ERROR in chatkit_endpoint: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))