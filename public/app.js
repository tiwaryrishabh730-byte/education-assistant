document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('user-input');
    const targetLangInput = document.getElementById('target-lang');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');

    // Auto-resize textarea
    input.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value.trim() === '') {
            this.style.height = 'auto';
        }
    });

    // Handle enter key to submit (Shift+Enter for new line)
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            form.dispatchEvent(new Event('submit'));
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const text = input.value.trim();
        const targetLanguage = targetLangInput.value.trim();
        
        if (!text) return;

        // Reset input
        input.value = '';
        input.style.height = 'auto';
        sendBtn.disabled = true;

        // Add user message to UI
        addMessage(text, 'user');

        // Add loading indicator
        const loadingId = addLoadingIndicator();

        try {
            // Call the FastAPI endpoint
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    target_language: targetLanguage || ""
                })
            });

            const data = await response.json();
            
            // Remove loading indicator
            document.getElementById(loadingId).remove();

            // Render assistant response using Marked.js (imported in HTML)
            if (data.response) {
                const parsedHtml = window.marked ? window.marked.parse(data.response) : data.response;
                addMessage(parsedHtml, 'assistant', true);
            } else {
                addMessage("Sorry, I didn't get a proper response from the server.", 'assistant');
            }

        } catch (err) {
            document.getElementById(loadingId).remove();
            addMessage(`**Error:** ${err.message}`, 'assistant', true);
        } finally {
            sendBtn.disabled = false;
            input.focus();
        }
    });

    function addMessage(content, sender, isHtml = false) {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', sender);

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = sender === 'user' ? 'U' : '🎓';

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        
        if (isHtml) {
            bubbleDiv.innerHTML = content;
        } else {
            const p = document.createElement('p');
            p.textContent = content;
            bubbleDiv.appendChild(p);
        }

        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(bubbleDiv);
        
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('message', 'assistant');
        msgDiv.id = id;

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('avatar');
        avatarDiv.textContent = '🎓';

        const bubbleDiv = document.createElement('div');
        bubbleDiv.classList.add('bubble');
        
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
        
        bubbleDiv.appendChild(typingDiv);
        msgDiv.appendChild(avatarDiv);
        msgDiv.appendChild(bubbleDiv);
        
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
        
        return id;
    }

    function scrollToBottom() {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    }
});
