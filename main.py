from src.assistant import Assistant
from src.config import WELCOME_MESSAGE
from src.utils import is_server_running

def main():
    if not is_server_running():
        print("The model server is not running. Please start the server first.")
        return
    
    assistant = Assistant.get_instance()
    
    print(WELCOME_MESSAGE)
    
    while True:
        user_input = input("User:\n")
        
        if user_input.lower() == 'exit()' or user_input.lower() == 'quit()':
            print("Goodbye!")
            break
        
        response, function_calls = assistant.process_message(user_input)
        print(f"\nFunction Calls:\n{function_calls}")
        print(f"\nAssistant:\n{response}\n")

if __name__ == "__main__":
    main()