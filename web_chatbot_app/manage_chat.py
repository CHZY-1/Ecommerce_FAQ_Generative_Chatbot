import json
import os

# Define the path to the chat history JSON file
CHAT_HISTORY_PATH = "chat_history.json"

# Load chat history from the JSON file
def load_chat_history():
    global chat_history
    if os.path.exists(CHAT_HISTORY_PATH):
        with open(CHAT_HISTORY_PATH, "r") as file:
            chat_history = json.load(file)
    else:
        chat_history = []

# Save chat history to the JSON file
def save_chat_history():
    with open(CHAT_HISTORY_PATH, "w") as file:
        json.dump(chat_history, file, indent=4)

def add_user_message(message):
    chat_history.append({"user_message": message, "chatbot_response": None, "feedback": None})

def add_chatbot_response(response):
    chat_history[-1]["chatbot_response"] = response

def update_feedback(message, feedback_value):
    for entry in reversed(chat_history):
        if entry["chatbot_response"] == message:
            entry["feedback"] = feedback_value
            # print(f"Updated feedback for response: {message}")
            # print(f"New feedback value: {feedback_value}")
            break
    else:
        print(f"No matching chatbot response found for message: {message}")
    
    save_chat_history()  # Save the updated chat history back to the JSON file


# Initialize chat history on module import
load_chat_history()
