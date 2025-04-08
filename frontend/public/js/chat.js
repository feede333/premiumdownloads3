class AIChat {
    constructor() {
        this.container = document.querySelector('.chat-container');
        this.toggleBtn = document.querySelector('.chat-toggle');
        this.closeBtn = document.querySelector('.close-chat');
        this.messages = document.querySelector('.chat-messages');
        this.input = document.querySelector('.chat-input');
        this.sendBtn = document.querySelector('.send-message');
        
        // Solo mantener el endpoint de DeepSeek
        this.apiEndpoint = 'https://api.deepseek.com/v1/chat/completions';
        this.apiKey = 'sk-b69329a50fcc4a3eabcf4a8bb6639f03'; // Tu API key de DeepSeek
        
        // Mantener historial de mensajes
        this.messageHistory = [];
        
        this.conversations = JSON.parse(localStorage.getItem('chatConversations')) || [];
        this.currentConversationId = null;
        
        this.conversationsList = document.querySelector('.conversations-list');
        this.newChatBtn = document.querySelector('.new-chat-btn');
        
        this.statusIndicator = document.createElement('div');
        this.statusIndicator.className = 'connection-status';
        this.container.insertBefore(this.statusIndicator, this.messages);
        
        this.setupEventListeners();
        this.setupConversations();
        this.setupWebSocket();
    }

    setupEventListeners() {
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        this.closeBtn.addEventListener('click', () => this.toggleChat());
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    setupConversations() {
        this.newChatBtn.addEventListener('click', () => this.startNewConversation());
        this.loadConversations();
    }

    startNewConversation() {
        const conversation = {
            id: Date.now(),
            title: 'Nueva conversación',
            messages: [],
            date: new Date().toISOString()
        };

        this.conversations.unshift(conversation);
        this.currentConversationId = conversation.id;
        this.saveConversations();
        this.loadConversations();
        this.clearChat();
    }

    loadConversations() {
        this.conversationsList.innerHTML = '';
        
        this.conversations.forEach(conv => {
            const item = document.createElement('div');
            item.className = `conversation-item ${conv.id === this.currentConversationId ? 'active' : ''}`;
            
            item.innerHTML = `
                <span>${conv.title}</span>
                <button class="delete-conversation">
                    <i class="fas fa-trash"></i>
                </button>
            `;

            item.addEventListener('click', (e) => {
                if (!e.target.closest('.delete-conversation')) {
                    this.loadConversation(conv.id);
                }
            });

            item.querySelector('.delete-conversation').addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteConversation(conv.id);
            });

            this.conversationsList.appendChild(item);
        });
    }

    loadConversation(conversationId) {
        this.currentConversationId = conversationId;
        this.clearChat();
        
        const conversation = this.conversations.find(c => c.id === conversationId);
        if (conversation) {
            conversation.messages.forEach(msg => {
                this.addMessage(msg.sender, msg.content, msg.type);
            });
        }
        
        this.loadConversations(); // Actualizar selección activa
    }

    deleteConversation(conversationId) {
        this.conversations = this.conversations.filter(c => c.id !== conversationId);
        this.saveConversations();
        
        if (this.currentConversationId === conversationId) {
            this.currentConversationId = null;
            this.clearChat();
        }
        
        this.loadConversations();
    }

    clearChat() {
        this.messages.innerHTML = '';
        this.messageHistory = [];
        this.addMessage('AI', '¡Hola! Soy el asistente virtual. ¿En qué puedo ayudarte?', 'bot');
    }

    async sendMessage() {
        const message = this.input.value.trim();
        if (!message) return;

        this.addMessage('Tú', message, 'user');
        this.input.value = '';
        
        this.messageHistory.push({ role: 'user', content: message });

        try {
            this.addMessage('AI', 'Escribiendo...', 'bot typing');
            
            const response = await this.callDeepSeekAPI(this.messageHistory);
            
            const typingMsg = this.messages.querySelector('.typing');
            if (typingMsg) typingMsg.remove();

            this.messageHistory.push({ role: 'assistant', content: response });
            this.addMessage('AI', response, 'bot');

            if (this.currentConversationId) {
                const conversation = this.conversations.find(c => c.id === this.currentConversationId);
                if (conversation) {
                    // Actualizar título si es el primer mensaje
                    if (conversation.messages.length === 0) {
                        conversation.title = message.substring(0, 30) + (message.length > 30 ? '...' : '');
                    }
                    
                    conversation.messages.push({
                        sender: 'Tú',
                        content: message,
                        type: 'user'
                    });
                    
                    // Agregar respuesta del bot
                    conversation.messages.push({
                        sender: 'AI',
                        content: response,
                        type: 'bot'
                    });
                    
                    this.saveConversations();
                    this.loadConversations();
                }
            }

        } catch (error) {
            console.error('Error:', error);
            this.addMessage('AI', 'Lo siento, hubo un error al procesar tu mensaje.', 'bot error');
        }
    }

    async callDeepSeekAPI(messages) {
        const response = await fetch(this.apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify({
                model: 'deepseek-chat',
                messages: messages,
                temperature: 0.7,
                max_tokens: 2000,
                stream: false
            })
        });

        if (!response.ok) {
            throw new Error('Error en la llamada a la API');
        }

        const data = await response.json();
        return data.choices[0].message.content;
    }

    addMessage(sender, text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        // Procesar el texto con formato
        const formattedText = this.formatText(text);
        
        messageDiv.innerHTML = `
            <div class="message-header">${sender}</div>
            <div class="message-content">${formattedText}</div>
        `;
        
        this.messages.appendChild(messageDiv);
        this.messages.scrollTop = this.messages.scrollHeight;
    }

    formatText(text) {
        return text
            // Enlaces [texto](url)
            .replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
            
            // Negritas con **
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            
            // Cursivas con *
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            
            // Títulos ###
            .replace(/###\s+([^\n]+)/g, '<h3>$1</h3>')
            
            // Listas con -
            .replace(/^\s*-\s+([^\n]+)/gm, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
            
            // Saltos de línea
            .replace(/\n/g, '<br>')
            
            // Preservar emojis
            .replace(/:[a-zA-Z0-9_+-]+:/g, match => {
                return match; // Mantener emojis intactos
            });
    }

    toggleChat() {
        this.container.classList.toggle('active');
    }

    saveConversations() {
        localStorage.setItem('chatConversations', JSON.stringify(this.conversations));
    }

    setupWebSocket() {
        try {
            this.ws = new WebSocket('ws://localhost:8080');
            
            this.ws.onopen = () => {
                console.log('Conectado al servidor');
                this.statusIndicator.textContent = '🟢 Conectado';
                this.statusIndicator.classList.add('connected');
            };
            
            this.ws.onclose = () => {
                console.log('Desconectado del servidor');
                this.statusIndicator.textContent = '🔴 Desconectado';
                this.statusIndicator.classList.remove('connected');
                // Intentar reconectar cada 5 segundos
                setTimeout(() => this.setupWebSocket(), 5000);
            };
            
            this.ws.onerror = (error) => {
                console.error('Error de WebSocket:', error);
                this.statusIndicator.textContent = '🔴 Error de conexión';
                this.statusIndicator.classList.remove('connected');
            };
        } catch (error) {
            console.error('Error al configurar WebSocket:', error);
            this.statusIndicator.textContent = '🔴 Error de conexión';
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AIChat();
});