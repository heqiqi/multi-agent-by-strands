import os, json
from strands import Agent, tool
from strands_tools import file_read, shell, file_write
from strands.models import BedrockModel
from agents.designer_team import designer_team
from utils.constants import CLAUDE_SONNET_3_7
from utils.prompt_template import COORDINATOR_SYSTEM_PROMPT
from utils.utils import app_logger as logger 

#env variable configure
#os.environ["STRANDS_TOOL_CONSOLE_MODE"] = "enabled"
os.environ["BYPASS_TOOL_CONSENT"] = "true"

logger.info("应用程序启动")


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
        logger.info(json.dumps(kwargs["message"], indent=2, ensure_ascii=False))

claude_sonnet_3_7 = BedrockModel(
  model_id=CLAUDE_SONNET_3_7,
  temperature=0.3,
  streaming=True, # Enable/disable streaming
)

# Create coordinator Agent
coodinartor_agent = Agent(
    system_prompt=COORDINATOR_SYSTEM_PROMPT,
    model=claude_sonnet_3_7,
    tools=[file_read, designer_team],
    callback_handler=message_buffer_handler
)


#test designer team
response = coodinartor_agent("请帮我设计一个图片，不需要更多的工作，图片包含aws的log和贝索斯照片.")
