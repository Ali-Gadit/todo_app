from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from .tools import add_task, list_tasks, complete_task, delete_task, update_task

# Critical: Load .env before accessing API keys
load_dotenv()

# Get API key
API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    # We raise an error if key is missing to ensure the agent doesn't fail silently later
    raise ValueError("GROQ_API_KEY environment variable is required in .env file")

# Initialize OpenAI-compatible client for Groq
external_client = AsyncOpenAI(
    api_key=API_KEY,
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