document.addEventListener('DOMContentLoaded', function() {
    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/'
    );

    chatSocket.onopen = function(e) {
        console.log('WebSocket connection established');
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const chatBox = document.getElementById('chat-box');

        // Create a new message element
        const messageElement = document.createElement('p');
        messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.message}`;

        // Append the message to the chat box
        chatBox.appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('WebSocket connection closed unexpectedly');
    };

    // Send a message when the send button is clicked
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message');

    sendButton.addEventListener('click', function() {
        const message = messageInput.value;
        if (message.trim() !== '') {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInput.value = '';
        }
    });
});
