import ell
from src.config import MODEL_NAME, TOOLS_PATH
from src.utils import load_system_prompt, create_functions_schema
from src.engine import FunctionCallingEngine
import openai
from src.config import API_KEY, BASE_URL

class OpenAIClient:
    """
    Singleton class for OpenAI client.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = openai.Client(
                api_key=API_KEY,
                base_url=BASE_URL,
            )
        return cls._instance

# Initialize the engine
ENGINE = FunctionCallingEngine()
ENGINE.add_functions_from_file(TOOLS_PATH)

# Load system prompt
SYSTEM_PROMPT = load_system_prompt(create_functions_schema(ENGINE.functions))

@ell.complex(
        model=MODEL_NAME, 
        client=OpenAIClient.get_instance(),
        stop=["<|end_function_calls|>"]
)
def ai_assistant(message_history: list[ell.Message]):
    return [
        ell.system(SYSTEM_PROMPT),
    ] + message_history