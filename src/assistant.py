from typing import List, Tuple, Any, Dict
import ell
from src.model import ai_assistant, SYSTEM_PROMPT, ENGINE
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
        self.engine = ENGINE

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def process_message(self, user_input: str) -> Tuple[str, Dict[str, Any]]:
        """
        Process a message from the user
        in the multi-turn conversation.

        Args:
            user_input (str): The user's input.

        Returns:
            Tuple[str, Dict[str, Any]]: The assistant's response and execution results.
        """
        self.message_history.append(ell.user(user_input))
        response = ai_assistant(self.message_history).content[0].text
        
        self.message_history.append(ell.assistant(response))

        assistant_response, has_function_calls = parse_model_response(response)
        
        if has_function_calls:
            results = self.engine.execute_code(assistant_response)
            self.message_history.append(ell.user(f"<|function_results|>\n{results}\n<|end_function_results|>"))
            final_response = ai_assistant(self.message_history).content[0].text
            self.message_history.append(ell.assistant(final_response))
            return final_response, results
        else:
            return assistant_response, {}

    def reset_conversation(self):
        self.message_history = []
        self.engine.reset_session()