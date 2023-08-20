// Feedback

function displayChatbotMessage(message) {
    var chatBox = document.getElementById('chat-box');
    var chatbotMessageDiv = document.createElement('div');
    chatbotMessageDiv.className = 'message chatbot-message';
    chatbotMessageDiv.textContent = message;

    // Append the chatbot message div to the chat box
    chatBox.appendChild(chatbotMessageDiv);

    // After appending the chatbot message div, insert feedback buttons
    insertFeedbackButtons(chatbotMessageDiv);

    // Scroll the chat box to show the new message
    chatBox.scrollTop = chatBox.scrollHeight;

    feedbackGiven = false;
}

// UI

function handleInputKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {

    // user input from input field
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
        sendUserMessageToServer(userMessage);
    }
}

function displayUserMessage(message) {
    var chatBox = document.getElementById('chat-box');
    var userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user-message';
    userMessageDiv.textContent = message;
    chatBox.appendChild(userMessageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendUserMessageToServer(message) {
    // user message to send in the POST request
    const data = {
        message: message
    };

    console.log(message)

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
        console.log(data.response)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}