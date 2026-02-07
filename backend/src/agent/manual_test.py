import asyncio
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

# Load env vars
load_dotenv()

from src.agent.agent import todo_agent
from agents import Runner, RunConfig, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

async def main():
    print("--- Agentic Tool Verification ---")
    
    # Configuration for Groq
    API_KEY = os.getenv("GROQ_API_KEY")
    if not API_KEY:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
    model = OpenAIChatCompletionsModel(openai_client=client, model="llama-3.3-70b-versatile")
    run_config = RunConfig(model=model, model_provider=client)

    # We use a dummy user_id "1" for testing
    # In a real app, this would come from the auth context
    context = {"user_id": "1"}
    
    print("\n1. Testing Agent Task Creation...")
    # Note: We need to tell the agent the user_id somehow. 
    # For this test, we'll explicitly mention it or assume the agent can ask.
    # The tools require user_id.
    
    prompt = "Add a task for user 1: Buy groceries (milk, eggs, bread)"
    print(f"User: {prompt}")
    
    result = await Runner.run(todo_agent, prompt, run_config=run_config)
    print(f"Agent: {result.final_output}")
    
    print("\n2. Testing Agent Task Listing...")
    prompt = "Show my pending tasks for user 1"
    print(f"User: {prompt}")
    result = await Runner.run(todo_agent, prompt, run_config=run_config)
    print(f"Agent: {result.final_output}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error running manual test: {e}")
        import traceback
        traceback.print_exc()