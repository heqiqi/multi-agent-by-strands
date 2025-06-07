from constants import REVIEWER_SYSTEM_PROMPT
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import editor, file_read, file_write, python_repl, shell
import os

@tool
def code_reviewer(code_folder: str) -> str:
    """
    Reviews Java code to a implement best practices

    Args:
        code: Java project folder.

    Returns:
        code review result or code  in markdown files
    """
    try:
        code_reviewer = Agent(
            system_prompt=REVIEWER_SYSTEM_PROMPT,
            tools=[shell, file_read, file_write]
        )
        result = str(code_reviewer(f"Review code in folder: {code_folder}")).strip()
        return result or "Code review did not return any result."
    except Exception as e:
        return f"Error reviewing code: {e}"
