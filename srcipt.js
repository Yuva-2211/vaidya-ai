

const API_URL = "http://127.0.0.1:8000/ask"; // Change when deploying




const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const messagesContainer = document.getElementById('messages');
const emptyState = document.getElementById('emptyState');
const typingIndicator = document.getElementById('typingIndicator');



messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});




async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Disable button to prevent spam clicks
    sendButton.disabled = true;

    emptyState.classList.add('hidden');
    addMessage(message, 'user');
    messageInput.value = '';

    typingIndicator.classList.add('active');
    scrollToBottom();

    try {
        const aiResponse = await callRAGBackend(message);
        addMessage(aiResponse, 'ai');
    } catch (error) {
        addMessage("Sorry, something went wrong. Please try again.", 'ai');
        console.error("Error:", error);
    }

    typingIndicator.classList.remove('active');
    sendButton.disabled = false;
}



async function callRAGBackend(userMessage) {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: userMessage   // Must match FastAPI model
        })
    });

    if (!response.ok) {
        throw new Error(`Server Error: ${response.status}`);
    }

    const data = await response.json();

    // FastAPI returns { "answer": "..." }
    return data.answer;
}



function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = type === 'user' ? 'YOU' : 'AYURVEDIC AI';

    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;

    messageDiv.appendChild(label);
    messageDiv.appendChild(content);
    messagesContainer.appendChild(messageDiv);

    scrollToBottom();
}




function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function sendSuggestion(suggestion) {
    messageInput.value = suggestion;
    sendMessage();
}
