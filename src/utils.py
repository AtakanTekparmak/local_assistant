import json
from typing import Dict, Callable, Tuple, List
import inspect
from typing import Any
from src.config import SYSTEM_PROMPT_PATH, FEWSHOT_PATH
from src.engine import FunctionCall, Parameter

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
            return between_tags, True
        else:
            return content, False
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from function calls")
        return [], False
    
def parse_function_calls(function_calls: str) -> List[FunctionCall]:
    """
    Parses the function calls from the model response.

    Example:
    weather_forecast = get_weather(city='Istanbul')
    success, file_path = save_to_file(content=weather_forecast, filename='weather_forecast.txt')
    """
    # Split the content by new lines
    function_calls_list: List[str] = function_calls.split("\n")

    # If there are empty lines, remove them
    function_calls_list = [call for call in function_calls_list if call.strip() != ""]

    parsed_function_calls: List[FunctionCall] = []

    for function_call in function_calls_list:
        # Return variable(s) are before the first =
        return_variables_str, function_call_str = function_call.strip().split(" = ", maxsplit=1)

        # If there is a comma, split the return variables
        if "," in return_variables_str:
            return_variables = return_variables_str.split(",")
        else:
            return_variables = [return_variables_str]

        # Turn the return variables into a list of strings
        return_variables = [str(var) for var in return_variables]

        # Turn the return variables into a list of Parameters
        return_variables = [Parameter(name=var, type="str") for var in return_variables]

        # The function call format is:
        # function_name(param1=value1, param2=value2, ...)
        # Extract the function name
        function_name = str(function_call_str.split("(")[0])

        # Remove the function name and the parentheses
        function_call_str = function_call_str.replace(function_name, "")
        function_call_str = function_call_str.replace("(", "")
        function_call_str = function_call_str.replace(")", "")

        # Split the function call string by commas if there are multiple parameters
        if "," in function_call_str:
            parameters = function_call_str.split(",")
        else:
            parameters = [function_call_str]

        # Create a dictionary of parameters
        parameters_dict = {param.split("=")[0].strip(): param.split("=")[1].replace("'", "").strip() for param in parameters}

        #import pdb; pdb.set_trace()

        # Add the function call to the list
        parsed_function_calls.append(
            FunctionCall(
                name=function_name,
                parameters=parameters_dict,
                returns=return_variables
            )
        )
        
    return parsed_function_calls
        
        
        

        