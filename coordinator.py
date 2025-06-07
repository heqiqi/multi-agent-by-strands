from agents.developer_agent import developer
from constants import PROJECT_MANAGER_SYSTEM_PROMPT
from strands import Agent, tool
from strands_tools import file_read, shell, file_write, editor
import logging, os, json


logging.getLogger("strands").setLevel(logging.INFO)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)
#os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

def custom_callback_handler(**kwargs):
    # Process stream data
    if "data" in kwargs:
        print(f"MODEL OUTPUT: {kwargs['data']}"),
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        print(f"\nUSING TOOL: {kwargs['current_tool_use']['name']}")
    elif "message" in kwargs:
        print(json.dumps(kwargs["message"], indent=2, ensure_ascii=False))

def message_buffer_handler(**kwargs):
    # When a new message is created from the assistant, print its content
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        print(json.dumps(kwargs["message"], indent=2, ensure_ascii=False))

# Create supervisor Agent
project_manager_agent = Agent(
    system_prompt=PROJECT_MANAGER_SYSTEM_PROMPT,
    tools=[shell, file_read, file_write, developer],
    callback_handler=message_buffer_handler
)

response = project_manager_agent("请帮我将文件夹 ./airline-booking-main 中的代码，从java8升级到java17。")
