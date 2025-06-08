import os, sys, json
from strands import Agent, tool
from strands_tools import editor, file_read, file_write, python_repl, shell, http_request
from strands.models import BedrockModel
from utils.constants import CLAUDE_SONNET_3_7, NOVA_PRO
from utils.prompt_template import CODE_DEVELOPER_PROMPT, CODE_REVIEWER_PROMPT, OPERATION_DEVELOPER_PROMPT, TECH_TEAM_PROMPT, IMAGE_DESIGNER_PROMPT, PRODUCT_MANAGER_PROMPT, TESTER_PROMPT
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

nove_pro = BedrockModel(
  model_id=NOVA_PRO,
  temperature=0.5,
  streaming=True, # Enable/disable streaming
)

@tool
def tech_team(query: str) -> str:
    """
    Coordinate the development, testing, deployment, and operation of software products
    """    
    tech_team_agent = Agent(
        system_prompt=TECH_TEAM_PROMPT,
        model=claude_sonnet_3_7,
        tools=[code_developer, code_reviewer, tester, operation_developer, shell],
        callback_handler=message_buffer_handler
    )
    logger.info(f"query: {query}")
    result = tech_team_agent(query)
    logger.info(f"result: {result}")
    return str(result)

@tool
def code_developer(query: str) -> str:
    """
    code developer 
    """    
    code_developer_agent = Agent(
        system_prompt=CODE_DEVELOPER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[shell, file_write, file_read],
        callback_handler=None
    )
    logger.info(f"query: {query}")
    result = code_developer_agent(query)
    logger.info(f"result: {result}")
    return str(result)

@tool
def code_reviewer(query: str) -> str:
    """
    code reviewer 
    """    
    code_developer_agent = Agent(
        system_prompt=CODE_REVIEWER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[shell, file_write, file_read],
        callback_handler=None
    )
    logger.info(f"query: {query}")
    result = code_developer_agent(query)
    logger.info(f"result: {result}")
    return str(result)

@tool
def tester(query: str) -> str:
    """
    code tester 
    """    
    tester_agent = Agent(
        system_prompt=TESTER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[shell, file_write, file_read],
        callback_handler=None
    )
    logger.info(f"query: {query}")
    result = tester_agent(query)
    logger.info(f"result: {result}")
    return str(result)

@tool
def operation_developer(query: str) -> str:
    """
    infra operation developer, operator
    """    
    operation_developer_agent = Agent(
        system_prompt=OPERATION_DEVELOPER_PROMPT,
        model=claude_sonnet_3_7,
        tools=[shell, file_write, file_read],
        callback_handler=None
    )
    logger.info(f"query: {query}")
    result = operation_developer_agent(query)
    logger.info(f"result: {result}")
    return str(result)

