from flask import Flask, render_template, request, jsonify
from chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

# root
@app.route('/')
def index():
    return render_template('chatbot_ui.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    # response = chatbot.generate_response(user_message)
    return jsonify({'response': user_message})

if __name__ == '__main__':
    app.run(debug=True)