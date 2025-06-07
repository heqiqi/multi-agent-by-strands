import os, sys, json
from strands import Agent, tool
from strands_tools import editor, file_read, file_write, python_repl, shell, http_request
from strands.models import BedrockModel
from utils.constants import CLAUDE_SONNET_3_7
from utils.prompt_template import DESINGER_TEAM_PROMPT, IMAGE_DESIGNER_PROMPT, PRODUCT_MANAGER_PROMPT
from utils.utils import app_logger as logger 



def custom_callback_handler(**kwargs):
    # Process stream data\n",
    if "data" in kwargs:
        print(f"MODEL OUTPUT: {kwargs['data']}"),
    elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
        print(f"\nUSING TOOL: {kwargs['current_tool_use']['name']}")

def message_buffer_handler(**kwargs):
    # When a new message is created from the assistant, print its content
    if "message" in kwargs and kwargs["message"].get("role") == "assistant":
        print(json.dumps(kwargs["message"], indent=2, ensure_ascii=False))


claude_sonnet_3_7 = BedrockModel(
  model_id=CLAUDE_SONNET_3_7,
  temperature=0.5,
  streaming=True, # Enable/disable streaming
)

@tool
def designer_team(query: str) -> str:
    """
    协调图片设计，产品需求和用户UI设计的工作
    """    
    designer_team_agent = Agent(
        system_prompt=DESINGER_TEAM_PROMPT,
        model=claude_sonnet_3_7,
        tools=[product_manager, image_designer],
        callback_handler=message_buffer_handler
    )
    logger.info(f"designer_team query: {query}")
    result = designer_team_agent(query)
    logger.info(f"designer_team result: {result}")
    return str(result)

@tool
def product_manager(query: str) -> str:
    """
    产品设计专家，整理产品信息，定义产品的功能，并给出用户图片生成的提示词
    """    
    product_manager_agent = Agent(
        system_prompt=PRODUCT_MANAGER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[http_request, shell, file_write],
        callback_handler=None
    )
    logger.info(f"product_manager query: {query}")
    result = product_manager_agent(query)
    logger.info(f"product_manager result: {result}")
    return str(result)

@tool
def image_designer(query: str) -> str:
    """
    图片设计师，按照要求设计出符合用户需求的图片或UI界面。
    """    
    image_designer_agent = Agent(
        system_prompt=IMAGE_DESIGNER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[shell, file_read, file_write],
        callback_handler=None
    )
    logger.info(f"image_designer query: {query}")
    result = image_designer_agent(query)
    logger.info(f"image_designer result: {result}")
    return str(result)
