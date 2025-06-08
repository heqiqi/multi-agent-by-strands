from utils.prompt_template import DATA_ANALYST_PROMPT, REVIEWER_SYSTEM_PROMPT
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import editor, file_read, file_write, python_repl, shell
import os

@tool
def data_analyst(query: str) -> str:
    """
    data analyst
    """
    try:
        data_analyst_agent = Agent(
            system_prompt=DATA_ANALYST_PROMPT,
            tools=[shell, file_read, file_write]
        )
        result = str(data_analyst_agent(query).strip())
        return result or "Data is empty and  result is none."
    except Exception as e:
        return f"Error  data fetch: {e}"
