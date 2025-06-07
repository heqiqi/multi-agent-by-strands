from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

aws_docs_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.aws-documentation-mcp-server@latest"]))
)

# {
#   "mcpServers": {
#     "awslabs.cost-analysis-mcp-server": {
#       "command": "uvx",
#       "args": ["awslabs.cost-analysis-mcp-server@latest"],
#       "env": {
#         "FASTMCP_LOG_LEVEL": "ERROR",
#         "AWS_PROFILE": "your-aws-profile"
#       },
#       "disabled": false,
#       "autoApprove": []
#     }
#   }
# }

aws_cost_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.cost-analysis-mcp-server@latest"], env={ "FASTMCP_LOG_LEVEL": "ERROR"}))
)

# {
#   "mcpServers": {
#     "awslabs.cloudwatch-logs-mcp-server": {
#       "autoApprove": [],
#       "disabled": false,
#       "timeout": 60,
#       "command": "uvx",
#       "args": [
#         "awslabs.cloudwatch-logs-mcp-server@latest",
#       ],
#       "env": {
#         "AWS_PROFILE": "[The AWS Profile Name to use for AWS access]",
#         "AWS_REGION": "[The AWS region to run in]",
#         "FASTMCP_LOG_LEVEL": "ERROR"
#       },
#       "transportType": "stdio"
#     }
#   }
# }

aws_cloudwatch_logs_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.cloudwatch-logs-mcp-server@latest"], env={ "FASTMCP_LOG_LEVEL": "ERROR", "AWS_REGION": "us-east-1"}))
)

# {
#   "mcpServers": {
#     "awslabs.nova-canvas-mcp-server": {
#       "command": "uvx",
#       "args": ["awslabs.nova-canvas-mcp-server@latest"],
#       "env": {
#         "AWS_PROFILE": "your-aws-profile",
#         "AWS_REGION": "us-east-1",
#         "FASTMCP_LOG_LEVEL": "ERROR"
#       },
#       "disabled": false,
#       "autoApprove": []
#     }
#   }
# }

aws_canvas_client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="uvx", args=["awslabs.nova-canvas-mcp-server@latest"], env={ "AWS_PROFILE":"default", "FASTMCP_LOG_LEVEL": "ERROR", "AWS_REGION": "us-east-1"}))
)