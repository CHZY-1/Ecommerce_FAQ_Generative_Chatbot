import json
import os

# Load chat history from the JSON file
def load_chat_history(chat_history_file):
    if os.path.exists(chat_history_file):
        with open(chat_history_file, "r") as file:
            chat_history = json.load(file)
    else:
        chat_history = []
    return chat_history

# Save chat history to the JSON file
def save_chat_history(chat_history, chat_history_file):
    with open(chat_history_file, "w") as file:
        json.dump(chat_history, file, indent=4)

def add_user_message(message, chat_history):
    chat_history.append({"user_message": message, "chatbot_response": None, "feedback": None})

def add_chatbot_response(response, chat_history):
    chat_history[-1]["chatbot_response"] = response

def update_feedback(message, feedback_value, chat_history, chat_history_file):

    # last entry allow feedback
    for entry in reversed(chat_history):

        # Check if the chatbot response in this entry matches the specified message.
        if entry["chatbot_response"] == message:
            # update the feedback value
            entry["feedback"] = feedback_value

            # print(f"Updated feedback for response: {message}")
            # print(f"New feedback value: {feedback_value}")
            break
    else:
        print(f"No matching chatbot response found for message: {message}")
    
    save_chat_history(chat_history, chat_history_file)  # Save the updated chat history back to the JSON file