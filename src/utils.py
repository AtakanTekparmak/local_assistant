import json
from typing import Dict, Callable, Tuple
import inspect
from typing import Any
from src.config import SYSTEM_PROMPT_PATH, FEWSHOT_PATH

def create_functions_schema(functions: Dict[str, Callable]) -> str:
    """
    Creates the functions schema for the prompt.
    """
    functions_schema = []
    for name, function in functions.items():
        try:
            annotations = function.__annotations__
            parameters = {
                param: annotations.get(param, Any).__name__
                for param in inspect.signature(function).parameters
                if param != 'return'
            }
            returns = annotations.get('return', Any).__name__
            
            metadata = {
                "name": name,
                "description": function.__doc__.replace('\\n', '\n') if function.__doc__ else "",
                "parameters": {"properties": parameters, "required": list(parameters.keys())},
                "returns": returns
            }
            functions_schema.append(metadata)
        except Exception as e:
            print(f"Error creating metadata for function {name}: {str(e)}")

    return json.dumps(functions_schema, indent=2, ensure_ascii=False)

def load_system_prompt(
        functions_schema: str,
        file_path: str = SYSTEM_PROMPT_PATH
    ) -> str:
    """
    Loads the system prompt from the specified file.
    """
    def replace_functions_schema(content: str) -> str:
        return content.replace("{{functions_schema}}", functions_schema)
    
    try:
        with open(file_path, "r") as file:
            return replace_functions_schema(file.read())
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    
def load_fewshot(
        file_path: str = FEWSHOT_PATH
    ) -> str:
    """
    Loads the fewshot from the specified file.
    """
    try:
        with open(file_path, "r") as file:
            file_content = json.load(file)
            
            assert isinstance(file_content, list), "Fewshot must be a list of messages"
            assert len(file_content) > 0, "Fewshot must not be empty"
            assert isinstance(file_content[0], dict), "Fewshot must be a list of dictionaries"
            assert "role" in file_content[0] and "content" in file_content[0], "Fewshot must be a list of dictionaries with 'role' and 'content' keys"
            assert file_content[0]["role"] == "user" and file_content[1]["role"] == "assistant", "Fewshot must be a list of dictionaries with 'role' key as 'user' or 'assistant'"
            
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {file_path}")
        return ""
    
def parse_model_response(content: str) -> Tuple[str, bool]:
    """
    Parses the model response to get the 
    assistant's response or function calls.

    Args:
        content (str): The model response.

    Returns:
        Tuple[str, bool]: The assistant's response and/or function calls.
    """

    if "```python" in content:
        content = content.split("```python")[1].split("```")[0]
        return content.strip(), True
    else:
        return content, False