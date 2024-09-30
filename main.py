from src.assistant import Assistant
from src.config import WELCOME_MESSAGE

def main():
    assistant = Assistant.get_instance()
    
    print(WELCOME_MESSAGE)
    
    while True:
        user_input = input("User:\n")
        
        if user_input.lower() == 'exit()' or user_input.lower() == 'quit()':
            print("Goodbye!")
            break
        
        response, function_calls = assistant.process_message(user_input)
        print(f"Function Calls:\n{function_calls}")
        print(f"Assistant:\n{response}")

if __name__ == "__main__":
    main()