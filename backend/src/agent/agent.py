from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from .tools import add_task, list_tasks, complete_task, delete_task, update_task
from ..config import settings

# Get API key from settings
API_KEY = settings.GROQ_API_KEY

# For backward compatibility or if settings doesn't have it yet
if not API_KEY:
    API_KEY = os.getenv("GROQ_API_KEY", "")

# We don't raise error here anymore to allow the app to start
# Validation happens when the client is used

# Initialize OpenAI-compatible client for Groq
external_client = AsyncOpenAI(
    api_key=API_KEY or "missing_key", # Use placeholder if empty to avoid pydantic error
    base_url="https://api.groq.com/openai/v1"
)

# Configure the model wrapper
model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="llama-3.3-70b-versatile"
)

# Set up run configuration
# This ensures the Runner uses the Groq client and model
run_config = RunConfig(
    model=model,
    model_provider=external_client,
)

# Disable strict schema for tools to avoid Groq validation issues with optional parameters
for tool in [add_task, list_tasks, complete_task, delete_task, update_task]:
    if hasattr(tool, "strict_json_schema"):
        tool.strict_json_schema = False

# Define the Todo Agent
todo_agent = Agent(
    name="Todo Agent",
    instructions=(
        "You are a helpful Todo assistant. Follow these behavioral guidelines:\n\n"
        "- **Task Creation**: When user mentions adding/creating/remembering something, use `add_task`.\n"
        "- **Task Listing**: When user asks to see/show/list tasks, use `list_tasks` with appropriate filter.\n"
        "- **Task Completion**: When user says done/complete/finished, use `complete_task`.\n"
        "- **Task Deletion**: When user says delete/remove/cancel, use `delete_task`.\n"
        "- **Task Update**: When user says change/update/rename, use `update_task`.\n"
        "- **Confirmation**: Always confirm actions with a friendly response.\n"
        "- **Error Handling**: Gracefully handle task not found and other errors.\n\n"
        "Natural Language Command Mappings:\n"
        "- 'Add a task to buy groceries' -> `add_task(title='Buy groceries')`\n"
        "- 'Show me all my tasks' -> `list_tasks(status='all')`\n"
        "- 'What's pending?' -> `list_tasks(status='pending')`\n"
        "- 'Mark task 3 as complete' -> `complete_task(task_id=3)`\n"
        "- 'Delete the meeting task' -> `list_tasks` first to find ID, then `delete_task`.\n"
        "- 'Change task 1 to \"Call mom tonight\"' -> `update_task(task_id=1, title='Call mom tonight')`\n"
        "- 'I need to remember to pay bills' -> `add_task(title='Pay bills')`\n"
        "- 'What have I completed?' -> `list_tasks(status='completed')`"
    ),
    tools=[add_task, list_tasks, complete_task, delete_task, update_task],
)