import json
from typing import Dict, Callable, Tuple
import inspect
from typing import Any
from src.config import SYSTEM_PROMPT_PATH

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
            returns = [{"name": f"{name}_output", "type": annotations.get('return', Any).__name__}]
            
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
    
def parse_model_response(content: str) -> Tuple[str, bool]:
    """
    Parses the model response to get the 
    assistant's response or function calls.

    Args:
        content (str): The model response.

    Returns:
        Tuple[str, bool]: The assistant's response and/or function calls.
    """
    # Remove the dollar signs from the JSON string
    content = content.replace("$", "")
    
    # If the assistant is generating new user input, cut it
    if "User:" in content:
        content = content.split("User:")[0]
    try:
        if "<|function_calls|>" in content: 
            between_tags = content.split("<|function_calls|>")[1]
            if "<|end_function_calls|>" in between_tags:
                between_tags = between_tags.split("<|end_function_calls|>")[0]
            return json.loads(between_tags), True
        elif "<|answer|>" in content:
            answer = content.split("<|answer|>")[1]
            answer = answer.split("<|end_answer|>")[0] if "<|end_answer|>" in answer else answer

            # If there are thoughts after the answer, cut them
            if "<|thoughts|>" in answer:
                answer = answer.split("<|thoughts|>")[0]
                
            return answer.strip(), False
        else:
            return content, False
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from function calls")
        return [], False