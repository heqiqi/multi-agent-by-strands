import os, sys, json
from strands import Agent, tool
from strands_tools import editor, file_read, file_write, python_repl, shell, http_request, generate_image
from strands.models import BedrockModel
from utils.constants import CLAUDE_SONNET_3_7
from utils.prompt_template import DESINGER_TEAM_PROMPT, IMAGE_DESIGNER_PROMPT, PRODUCT_MANAGER_PROMPT
from utils.utils import app_logger as logger 
from tools.aws_mcp import aws_canvas_client

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
    Coordinate image design, product requirements, and user interface design work
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
    Product design experts organize product information, define product features, and provide prompts for user image generation
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
    Image designer, design images or UI interfaces that meet user needs according to requirements
    """
    result = str()
    with aws_canvas_client:
        mcp_tools = aws_canvas_client.list_tools_sync()
        image_designer_agent = Agent(
            system_prompt=IMAGE_DESIGNER_PROMPT,
            model=claude_sonnet_3_7,
            tools=[shell, file_read, file_write,mcp_tools, generate_image],
            callback_handler=None
        )
        logger.info(f"image_designer query: {query}")
        result = image_designer_agent(query)
    logger.info(f"image_designer result: {result}")
    return str(result)
