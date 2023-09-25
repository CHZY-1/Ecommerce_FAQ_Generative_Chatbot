var chatHistory = []
var botResponding = false;

// UI Functions
function handleInputKey(event) {
    if (event.key === 'Enter' && !botResponding) {
        sendMessage();
    }
}

function sendMessage() {
    var userInput = document.getElementById('user-input');
    var userMessage = userInput.value.trim();

    if (userMessage !== '') {
        // Display user message
        displayUserMessage(userMessage);
        
        // stop user from entering question when chatbot is generating response
        userInput.disabled = true;
        botResponding = true;

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

// function displayChatbotMessage(message) {
//     // Check if the message already exists in the chat history
//     if (!chatHistory.some(entry => entry.sender === 'chatbot' && entry.message === message)) {
//         if (message.toLowerCase().includes("start over") || message.toLowerCase().includes("reset")) {
//             displayMessage(message, 'chatbot', false, true);
//         } else {
//             displayMessage(message, 'chatbot');
//         }
//         // Update chat history
//         chatHistory.push({ sender: 'chatbot', message: message });
//     }
// }


// Display a chatbot message in the interface
function displayChatbotMessage(message) {

    if (message.toLowerCase().includes("start over") || message.toLowerCase().includes("reset")) {
        // Display the message as a special reset message
        displayMessage(message, 'chatbot', false, true);
    } 
    else {
        // /Display a chatbot message and store it in the chat history
        displayMessage(message, 'chatbot');
        chatHistory.push({ sender: 'chatbot', message: message });
    }
}

// Display message in the interface
function displayMessage(message, sender, hideFeedback = false, isReset = false) {
    var chatBox = document.getElementById('chat-box');
    var messageDiv = document.createElement('div');
    
    if (isReset) {
        // Display a reset message
        messageDiv.className = 'message reset-message';
        messageDiv.textContent = message;
    } else {
        // Display user or chatbot message
        messageDiv.className = sender === 'chatbot' ? 'message chatbot-message' : 'message user-message';
        messageDiv.innerHTML = sender === 'chatbot' ? `<span class="message-label">Assistant:</span> ${message}` : `<span class="message-label">User:</span> ${message}`;
        
        // show feedback button
        if (sender === 'chatbot' && !hideFeedback) {
            insertFeedbackButtons(messageDiv);
        }
    }
    
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    feedbackGiven = false;
}

// Communicate with server
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

        // allow user to enter question after response is generated and displayed
        var userInput = document.getElementById('user-input');
        userInput.disabled = false;
        botResponding = false;

        userInput.focus();

    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Event Listeners
window.onload = function() {
    displayMessage("Hi there! How can I assist you ?", 'chatbot', true, false);
    // displayChatbotMessage("Hi there! How can I assist you?");
    var userInput = document.getElementById('user-input');
    userInput.focus();
};
