from typing import List, Tuple, Any, Dict
import ell
from src.model import ai_assistant, SYSTEM_PROMPT
from src.engine import ToolCallingEngine
from src.utils import parse_model_response

class Assistant:
    """
    Singleton multi-turn conversation assistant.
    """
    _instance = None

    def __init__(self):
        self.message_history: List[ell.Message] = [
            ell.system(SYSTEM_PROMPT)
        ]
        self.engine = ToolCallingEngine.get_instance()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def process_message(self, user_input: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Process a message from the user
        in the multi-turn conversation.

        Args:
            user_input (str): The user's input.

        Returns:
            str: The assistant's response.
        """
        self.message_history.append(ell.user(user_input))
        response = ai_assistant(self.message_history).content[0].text
        
        # Get the assistant message and append it to the message history
        self.message_history.append(ell.assistant(response))

        # If the assistant message has tool calls,
        # Parse function calls or assistant response from model response
        assistant_response, success = parse_model_response(response)
        
        if success: 
            results = self.engine.parse_and_call_functions(assistant_response)
            self.message_history.append(ell.user(f"<|function_results|>\n{results}\n<|end_function_results|>"))
            final_response = ai_assistant(self.message_history).content[0].text
            self.message_history.append(ell.assistant(final_response))
            return final_response, assistant_response
        else:
            return assistant_response, None

    def reset_conversation(self):
        self.message_history = []