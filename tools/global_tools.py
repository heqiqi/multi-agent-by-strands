from strands_tools import file_read, shell, file_write
from tools.aws_mcp import aws_docs_client, aws_cost_client, aws_cloudwatch_logs_client, aws_canvas_client

# Define all tools that should be globally available
GLOBAL_TOOLS = [
    file_read,
    shell,
    file_write,
    aws_docs_client,
    aws_cost_client,
    aws_cloudwatch_logs_client,
    aws_canvas_client
]

# Function to get all available tools
def get_all_tools():
    return GLOBAL_TOOLS