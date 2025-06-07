

APP_NAME = "multi-agent-by-strands"

DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s"
DEFAULT_LOG_FILE = f"logs/{APP_NAME}.log"

DEFAULT_SERVER_PORT = 8080
MAX_RETRIES = 3

# Models
NOVA_PRO = "us.amazon.nova-pro-v1:0"
NOVA_PREMIER = "us.amazon.nova-premier-v1:0"
CLAUDE_OPUS = "us.anthropic.claude-opus-4-20250514-v1:0"
DEEPSEEK_R1 = "us.deepseek.r1-v1:0"
CLAUDE_SONNET_3_7 = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"