from typing import Tuple
import os

from src.config import OUTPUT_FOLDER


def save_to_file(
        content: str,
        filename: str,
    ) -> Tuple[bool, str]:
    """
    Save a string to a file.

    Args:
        content (Union[str, List[str]]): The content to save to the file. Can be a single string or a list of strings.
        filename (str): The name of the file to save the content to.
    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating whether the file was saved successfully and the path to the file.
    """
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        with open(f"{OUTPUT_FOLDER}/{filename}", "w") as file:
            file.write(content)
        return True, f"{OUTPUT_FOLDER}/{filename}"
    except OSError as e:
        print(f"Error creating output folder: {e}")
        return False, ""
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False, ""