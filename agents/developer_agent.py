
from strands import Agent, tool
from strands_tools import editor, file_read, file_write, python_repl, shell
import os

CODE_DEVELOPER_SYSTEM_PROMPT = """
# DEVELOPER AGENT

## Role and Identity
You are the Developer Agent in a multi-agent system. Your primary responsibility is to write high-quality, maintainable code based on specifications and requirements provided to you. You excel at translating requirements into working software implementations.

## Core Responsibilities
- Implement software solutions based on provided specifications
- Write clean, efficient, and well-documented code
- Follow best practices and coding standards
- Create unit tests for your implementations
- Debug and fix issues in code

## Critical Rules
1. **ALWAYS write code that follows best practices** for the language/framework being used.
2. **ALWAYS include comprehensive comments** in your code to explain complex logic.
3. **ALWAYS consider edge cases** and handle exceptions appropriately.
4. **ALWAYS write unit tests** for your implementations when appropriate.

## File System Management
- Use absolute paths for all file references
- Organize code files according to project conventions
- Create appropriate directory structures for new features
- Maintain separation of concerns in your file organization

Remember: Your success is measured by how effectively you translate requirements into working, maintainable code that meets the specified needs while adhering to best practices.
"""

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

@tool
def code_develop_command(command: str) -> str:
    """
    Run code develop for modifying and assess code 
    
    Args:
        command: java developer task Command
        
    Returns:
        Command output as string
    """
    # ANSI color codes
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    print(f"{BLUE}run_shell_command Executing command:{RESET} {command}")
    
    # Run command, display the output in real-time, and capture output
    import subprocess
    import sys
    
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    result = ""
    for line in iter(process.stdout.readline, ''):
        print(line, end='')
        sys.stdout.flush()
        result += line
    
    process.stdout.close()
    process.wait()
    
    # Print colored output
    print(f"{GREEN}Output:{RESET}\n{result}")
    
    return result

@tool
def developer(query: str) -> str:
    """
    DEVELOPER AGENT, Developer Java code to a implement best practices

    Args:
        query: java developer command  for tools code_develop_command

    Returns:
        code review result or code  in markdown files
    """
    q_cmd = f"请使用code_develop_command，执行： q chat --no-interactive --trust-all-tools '{query}' "
    print(f"Developer is coding...q_cmd: {q_cmd}")
    developer_agent = Agent(
        system_prompt=CODE_DEVELOPER_SYSTEM_PROMPT,
        tools=[code_develop_command],
        callback_handler=None
    )
    result = developer_agent(q_cmd)
    print(f"developer result: {result}")
    return result

#developer("请对../airline-booking-main项目执行Java 8到Java 17修改任务，任务描述在 ../tasks/assessment_phase.md")
