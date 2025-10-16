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

