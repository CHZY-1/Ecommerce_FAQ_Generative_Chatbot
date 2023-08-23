var chatHistory = []

// UI Functions
function handleInputKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    var userInput = document.getElementById('user-input');
    var userMessage = userInput.value.trim();

    if (userMessage !== '') {
        // Display user message
        displayUserMessage(userMessage);

        // Clear the input field
        userInput.value = '';

        // Remove feedback buttons
        removeFeedbackButtons();

        // Send user message to server and receive response
        if (!feedbackGiven) {
            sendUserMessageToServer(userMessage);
        }
    }
}

// Display Functions
function displayUserMessage(message) {
    displayMessage(message, 'user');
    // Update chat history
    chatHistory.push({ sender: 'user', message: message });
}

function displayChatbotMessage(message) {
    // Check if the message already exists in the chat history
    if (!chatHistory.some(entry => entry.sender === 'chatbot' && entry.message === message)) {
        if (message.toLowerCase().includes("start over") || message.toLowerCase().includes("reset")) {
            displayMessage(message, 'chatbot', false, true);
        } else {
            displayMessage(message, 'chatbot');
        }
        // Update chat history
        chatHistory.push({ sender: 'chatbot', message: message });
    }
}


function displayMessage(message, sender, hideFeedback = false, isReset = false) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    
    if (isReset) {
        messageDiv.className = 'message reset-message';
        messageDiv.textContent = message;
    } else {
        messageDiv.className = sender === 'chatbot' ? 'message chatbot-message' : 'message user-message';
        messageDiv.innerHTML = sender === 'chatbot' ? `<span class="message-label">Assistant:</span> ${message}` : `<span class="message-label">User:</span> ${message}`;
        
        if (sender === 'chatbot' && !hideFeedback) {
            insertFeedbackButtons(messageDiv);
        }
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    feedbackGiven = false;
}

// Server Communication
function sendUserMessageToServer(message, feedbackValue = null) {
    // user message and feedback value
    const data = {
        message: message,
        feedback: feedbackValue
    };

    console.log(message);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Display the chatbot's response
        displayChatbotMessage(data.response);
        console.log(data.response);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Event Listeners
window.onload = function() {
    // displayChatbotMessage("Hi there! How can I assist you?");
    var userInput = document.getElementById('user-input');
    userInput.focus();
};
