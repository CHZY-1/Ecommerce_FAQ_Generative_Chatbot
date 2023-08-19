var feedbackGiven = false; // Initialize the feedback flag

// Function to give feedback
function giveFeedback() {
    if (!feedbackGiven) {
        // Set the flag to true to indicate that feedback has been given for this response
        feedbackGiven = true;

        var chatBox = document.getElementById('chat-box');
        var feedbackDiv = document.createElement('div');
        feedbackDiv.className = 'message feedback-message';

        feedbackDiv.textContent = "Thank you for your feedback!";

        // Append the feedback div to the chat box
        chatBox.appendChild(feedbackDiv);

        // Scroll the chat box to show the new message
        chatBox.scrollTop = chatBox.scrollHeight;

        // Remove the feedback buttons
        removeFeedbackButtons();
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

    // Use Material Icons for the button icons
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