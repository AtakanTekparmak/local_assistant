from typing import Union, Any, Dict
import importlib.util
import os
import traceback

from pydantic import BaseModel

# Declare type aliases
ValidParameter = Union[str, int, float, bool, dict, list, BaseModel]
ValidOutput = ValidParameter

# Declare constants
INVALID_FUNCTION_CALL_ERROR = """
The function call is invalid. 
"""


class PythonInterpreter:
    """
    A class that interprets Python code and executes functions.
    """
    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.locals: Dict[str, Any] = {}
        self.functions: Dict[str, callable] = {}

    def add_functions(self, functions: Dict[str, callable]) -> None:
        """
        Add functions to the interpreter's global namespace.

        Args:
            functions (Dict[str, callable]): A dictionary of functions to add to the interpreter.
        """
        self.globals.update(functions)


    def add_functions_from_file(self, file_path: str) -> None:
        """
        Add functions to the interpreter from a specified .py file.

        Args:
            file_path (str): The path to the file containing the functions to add.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found")

        module_name = os.path.basename(file_path).split('.')[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for name, obj in module.__dict__.items():
            if callable(obj) and not name.startswith("__"):
                self.globals[name] = obj

    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute Python code and return the updated local variables.

        Args:
            code (str): The Python code to execute.

        Returns:
            Dict[str, Any]: The updated local variables.
        """
        try:
            exec(code, self.globals, self.locals)
            return self.locals
        except Exception as e:
            return {"error": str(e), "traceback": traceback.format_exc()}

    def reset_session(self) -> None:
        """Reset the session of the interpreter."""
        self.locals.clear()

# Replace FunctionCallingEngine with PythonInterpreter
ENGINE = PythonInterpreter()