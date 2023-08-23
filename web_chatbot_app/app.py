from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

# functions
from manage_chat import load_chat_history, save_chat_history, add_user_message, add_chatbot_response, update_feedback

from manage_chat import chat_history # variable

app = Flask(__name__)

chatbot = None

@app.before_first_request
def initialize_chatbot():
    global chatbot
    chatbot = Chatbot(model="C:/Users/User/Desktop/tuned_dialogpt_Ecommerce_FAQ", 
                      tokenizer="microsoft/DialoGPT-large")
    # chatbot = Chatbot(model="C:/Users/User/Desktop/tuned_dialogpt_Ecommerce_FAQ", 
    #                   tokenizer="microsoft/DialoGPT-large")
    load_chat_history()
    print(chat_history)

@app.route('/')
def index():
    return render_template('chatbot_ui.html')

@app.route('/update_feedback_script', methods=['POST'])
def update_feedback_script():
    feedback_data = request.json
    message = feedback_data['message']
    feedback_value = feedback_data['feedback']

    update_feedback(message, feedback_value)
    save_chat_history()  # Save the updated chat history

    return jsonify({'message': 'Feedback value updated successfully from feedback script'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    feedback_value = data.get('feedback')  # Get feedback value from request data, it can be None
    
    add_user_message(user_message)
    response = chatbot.generate_response(user_message)
    add_chatbot_response(response)
    
    if feedback_value is not None:  # Only update feedback if it's provided
        update_feedback(response, feedback_value)
    
    save_chat_history()  # Save chat history after each interaction
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
