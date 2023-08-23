from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)

chatbot = None

@app.before_first_request
def initialize_chatbot():
    global chatbot
    # chatbot = Chatbot()
    chatbot = Chatbot(model="D:/tuned_dialogpt_Ecommerce_FAQ", 
                      tokenizer="microsoft/DialoGPT-large")

# root
@app.route('/')
def index():
    return render_template('chatbot_ui.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    response = chatbot.generate_response(user_message)

    print(response)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)