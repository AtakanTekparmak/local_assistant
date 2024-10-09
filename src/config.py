# General
MODEL_NAME = "qwen2.5-coder-7b-instruct"
BASE_URL = "http://192.168.68.58:1234/v1"
API_KEY = "test"    
SYSTEM_PROMPT_PATH = "src/static/system_prompt.txt"
FEWSHOT_PATH = "src/static/fewshot.json"
WELCOME_MESSAGE = """
Welcome to KantoorBot!

Type 'exit()' or 'quit()' to end the conversation.
"""

# Tools
WEB_SEARCH_MAX_RESULTS = 3
TOOLS_PATH = "src/tools/__init__.py"
OUTPUT_FOLDER = "output"