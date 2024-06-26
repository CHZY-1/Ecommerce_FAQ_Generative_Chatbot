from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

# functions
from manage_chat import load_chat_history, save_chat_history, add_user_message, add_chatbot_response, update_feedback
from intent_recogition import determine_intent

from transformers import pipeline, Conversation
# conversation = Conversation("")
# conversation = chatbot(conversation)
# conversation.generated_responses[-1]

app = Flask(__name__)

cs_chatbot = None
general_chatbot  = None

chat_history = []

CHAT_HISTORY_PATH = "chat_history.json"

@app.before_first_request
def initialize_chatbot():
    global cs_chatbot, general_chatbot, chat_history
    # chatbot = Chatbot()
    cs_chatbot = Chatbot(model="D:/fine_tuned_dialogpt_FAQ_Ecommerce_1", 
                      tokenizer="microsoft/DialoGPT-large")
    # cs_chatbot = Chatbot(model="C:/Users/User/Desktop/fine_tuned_dialogpt_FAQ_Ecommerce_1", 
    #                   tokenizer="microsoft/DialoGPT-large")
    
    general_chatbot = pipeline(model="microsoft/DialoGPT-medium")

    chat_history = load_chat_history(CHAT_HISTORY_PATH)
    # print(chat_history)

@app.route('/')
def index():
    return render_template('chatbot_ui.html')

@app.route('/update_feedback_script', methods=['POST'])
def update_feedback_script():
    feedback_data = request.json
    message = feedback_data['message']
    feedback_value = feedback_data['feedback']

    update_feedback(message, feedback_value, chat_history, CHAT_HISTORY_PATH)
    save_chat_history(chat_history, CHAT_HISTORY_PATH)  # Save the updated chat history

    return jsonify({'message': 'Feedback value updated successfully from feedback script'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    # Get feedback value from request data, it can be None
    feedback_value = data.get('feedback')  

    # Determine user intent (customer service or general)
    # intent = determine_intent(user_message)
    intent = "customer_service"
    # print(intent)
    # print(user_message)

    if intent == "customer_service":
        # use fine tuned model to generate response
        response = cs_chatbot.generate_response(user_message)
    else:
        # use general chatbot pipeline to generate response
        conversation = Conversation(user_message)
        conversation = general_chatbot(conversation, 
                                                  max_length=500, 
                                                  min_length=10, 
                                                  temperature=0.2, 
                                                  top_k=50, 
                                                  top_p=0.95, 
                                                  no_repeat_ngram_size=2, 
                                                  pad_token_id=general_chatbot.tokenizer.eos_token_id)
        response = conversation.generated_responses[-1]
    
    add_user_message(user_message, chat_history)
    add_chatbot_response(response, chat_history)
    
    if feedback_value is not None:  # Only update feedback if it's provided
        update_feedback(response, feedback_value)
    
    save_chat_history(chat_history, CHAT_HISTORY_PATH)  # Save chat history after each interaction
    
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
