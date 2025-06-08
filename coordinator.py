import os, json
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import editor, file_read,agent_graph
from agents.data_analyst import data_analyst
from agents.tech_team import tech_team
from agents.designer_team import designer_team
from utils.constants import CLAUDE_SONNET_3_7
from utils.prompt_template import COORDINATOR_SYSTEM_PROMPT, DATA_ANALYST_PROMPT, DESINGER_TEAM_PROMPT, TECH_TEAM_PROMPT
from utils.utils import app_logger as logger 
from tools.global_tools import GLOBAL_TOOLS, aws_canvas_client

#env variable configure
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
    tools=[file_read, designer_team, tech_team, data_analyst],
    callback_handler=message_buffer_handler
)

graph_agent = Agent(tools=[agent_graph])

# Create a research team with a star topology
result = graph_agent.tool.agent_graph(
    action="create",
    graph_id="total_team",
    topology={
        "type": "star",
        "nodes": [
            {
                "id": "coordinator",
                "role": "team_lead",
                "system_prompt": COORDINATOR_SYSTEM_PROMPT
            },
            {
                "id": "tech_team",
                "role": "tech team",
                "system_prompt": TECH_TEAM_PROMPT
            },
            {
                "id": "designer_team",
                "role": "designer team",
                "system_prompt": DESINGER_TEAM_PROMPT
            },
            {
                "id": "data_analyst",
                "role": "data expert for product performance analyst",
                "system_prompt":DATA_ANALYST_PROMPT
            }
        ],
        "edges": [
            {"from": "coordinator", "to": "tech_team"},
            {"from": "coordinator", "to": "designer_team"},
            {"from": "coordinator", "to": "data_analyst"},
            {"from": "data_analyst", "to": "coordinator"},
            {"from": "designer_team", "to": "coordinator"},
            {"from": "tech_team", "to": "coordinator"}
        ]
    }
)


def main():
    logger.info("应用程序启动")
    response = coodinartor_agent("请帮我设计一个图片，不需要更多的铲批设计工作，图片是海边的小屋.")
    logger.info(f"response: {response}")

if __name__ == "__main__":
    main()
