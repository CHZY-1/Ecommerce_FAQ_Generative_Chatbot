var feedbackGiven = false; // Initialize the feedback flag

function giveFeedback(isPositive) {
    if (!feedbackGiven) {
        feedbackGiven = true;

        var chatBox = document.getElementById('chat-box');
        var feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'message feedback-message';

        var feedbackMessage = isPositive ? 'Positive feedback received. Thank you!' : 'Negative feedback received. Thank you!';
        feedbackDiv.textContent = feedbackMessage;

        chatBox.appendChild(feedbackDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        // Get the last chatbot response and update its feedback value
        var lastChatbotResponse = getLastChatbotResponse();
        if (lastChatbotResponse !== '') {
            var feedbackValue = isPositive ? 1 : -1;
            updateFeedbackValue(lastChatbotResponse, feedbackValue);
            sendUpdatedFeedbackValue(lastChatbotResponse, feedbackValue);

            // Update chat history
            chatHistory.forEach(entry => {
                if (entry.message === lastChatbotResponse) {
                    entry.feedback = feedbackValue;
                }
            });
        }

        removeFeedbackButtons();

        var userInput = document.getElementById('user-input');
        userInput.focus();
    }
}


// Function to remove feedback buttons
function removeFeedbackButtons() {
    var feedbackButtons = document.getElementsByClassName('feedback-buttons')[0];
    if (feedbackButtons) {
        feedbackButtons.remove();
    }
}

// Function to insert feedback buttons after the chatbot message div
function insertFeedbackButtons(chatbotMessageDiv) {
    var feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'feedback-buttons';

    feedbackDiv.innerHTML = `
        <button class="feedback-button positive" onclick="giveFeedback(true)">
            <span class="material-icons">thumb_up</span>
        </button>
        <button class="feedback-button negative" onclick="giveFeedback(false)">
            <span class="material-icons">thumb_down</span>
        </button>
    `;

    chatbotMessageDiv.appendChild(feedbackDiv);
}

// Helper function to get the last chatbot response
function getLastChatbotResponse() {
    var lastResponse = '';
    for (var i = chatHistory.length - 1; i >= 0; i--) {
        if (chatHistory[i].sender === 'chatbot') {
            lastResponse = chatHistory[i].message;
            break;
        }
    }
    return lastResponse;
}

// Helper function to update feedback value in chat history
function updateFeedbackValue(message, feedbackValue) {
    for (var i = chatHistory.length - 1; i >= 0; i--) {
        if (chatHistory[i].message === message) {
            chatHistory[i].feedback = feedbackValue;
            break;
        }
    }
}

function sendUpdatedFeedbackValue(message, feedbackValue) {
    const data = {
        message: message,
        feedback: feedbackValue
    };

    fetch('/update_feedback_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}