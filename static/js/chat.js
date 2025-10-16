// This file handles the real-time chat functionality for messaging between users

class Chat {
    constructor(conversationId) {
        // Set up the chat with the current conversation
        this.conversationId = conversationId;  // Which conversation we're in
        this.messagesContainer = document.getElementById('chat-messages');  // Where messages appear
        this.messageForm = document.getElementById('message-form');  // The message sending form
        this.messageInput = document.getElementById('message-input');  // The message text box
        this.loading = false;  // Track if we're currently loading messages

        this.init();  // Start up the chat system
    }

    init() {
        // Set up the chat when page loads
        this.loadMessages();  // Load existing messages
        this.setupEventListeners();  // Set up click and typing handlers

        // Check for new messages every 5 seconds
        setInterval(() => this.loadMessages(), 5000);
    }

    setupEventListeners() {
        // Handle message form submission
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();  // Stop normal form submission
            this.sendMessage();  // Send message using AJAX
        });

        // Auto-resize message input as user types
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';  // Reset height
            // Grow up to 120px tall, but no taller
            this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
        });
    }

    async loadMessages() {
        // Don't load if we're already loading messages
        if (this.loading) return;

        this.loading = true;  // Mark as loading
        try {
            // Ask server for latest messages
            const response = await fetch(`/items/conversations/${this.conversationId}/messages/`);
            const data = await response.json();  // Parse JSON response

            if (data.messages) {  // If we got messages back
                this.renderMessages(data.messages);  // Show them in the chat
            }
        } catch (error) {
            // If something went wrong, log error but don't crash
            console.error('Error loading messages:', error);
        } finally {
            this.loading = false;  // No longer loading
        }
    }
renderMessages(messages) {
        // Clear current messages and show new ones
        this.messagesContainer.innerHTML = '';  // Empty the container

        // Create and add each message to the chat
        messages.forEach(message => {
            const messageElement = this.createMessageElement(message);
            this.messagesContainer.appendChild(messageElement);
        });

        this.scrollToBottom();  // Keep view at latest message
    }
createMessageElement(message) {
        // Create HTML element for a single message
        const messageDiv = document.createElement('div');
        // Add CSS class based on who sent the message
        messageDiv.className = `message-bubble ${message.is_own ? 'message-own' : 'message-other'}`;

        // Fill in the message content and info
        messageDiv.innerHTML = `
            <div class="message-content">${this.escapeHtml(message.content)}</div>
            <div class="message-info">
                ${message.is_own ? 'You' : message.sender} • ${message.created_at}
            </div>
        `;

        return messageDiv;
    }
async sendMessage() {
        // Send a new message to the server
        const content = this.messageInput.value.trim();  // Get message text

        if (!content) return;  // Don't send empty messages

        const formData = new FormData(this.messageForm);  // Get form data

        try {
            // Send message to server using AJAX
            const response = await fetch(this.messageForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',  // Identify as AJAX request
                    'X-CSRFToken': this.getCsrfToken()  // Security token
                }
            });

            if (response.ok) {  // If server accepted our message
                const data = await response.json();
                if (data.success) {  // If message was saved
                    this.messageInput.value = '';  // Clear input box
                    this.messageInput.style.height = 'auto';  // Reset height
                    this.addMessageToChat(data.message);  // Add to chat immediately
                }
            } else {
                throw new Error('Failed to send message');
            }
        } catch (error) {
            // Show error message if sending failed
            console.error('Error sending message:', error);
            alert('Error sending message. Please try again.');
        }
    }
