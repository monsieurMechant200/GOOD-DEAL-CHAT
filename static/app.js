// marked est disponible globalement via le CDN
let messages = [];

const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const loadingIndicator = document.getElementById('loading-indicator');

const WELCOME_MESSAGE = {
    role: 'assistant',
    content: "Bienvenue dans le chat  DATAIKOS. je me nomme Lisa, pour vous servir. **Posez une question sur Excel ou l'ingénierie de prompt** et laissez les étoiles répondre."
};

function addMessage(role, content) {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble', role);
    // Rendu Markdown → HTML
    if (role === 'assistant') {
        // On autorise un rendu propre ; marked échappe les scripts de base.
        // Pour une sécurité supplémentaire, on pourrait utiliser DOMPurify.
        bubble.innerHTML = marked.parse(content);
    } else {
        // Messages utilisateur : texte simple échappé
        bubble.textContent = content;
    }
    chatContainer.appendChild(bubble);
    messages.push({ role, content });
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function setLoading(isLoading) {
    loadingIndicator.style.display = isLoading ? 'block' : 'none';
    sendButton.disabled = isLoading;
    userInput.disabled = isLoading;
}

function handleSend() {
    const content = userInput.value.trim();
    if (!content) return;
    addMessage('user', content);
    userInput.value = '';
    userInput.style.height = 'auto';
    fetchAssistantReply();
}

async function fetchAssistantReply() {
    setLoading(true);
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages })
        });
        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.error || `Erreur ${response.status}`);
        }
        const data = await response.json();
        const assistantMsg = data.message.content;
        addMessage('assistant', assistantMsg);
    } catch (error) {
        console.error(error);
        addMessage('assistant', "_Désolé, une perturbation stellaire m'empêche de répondre. Réessayez._");
    } finally {
        setLoading(false);
    }
}

userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = userInput.scrollHeight + 'px';
});
sendButton.addEventListener('click', handleSend);
userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

// Initialisation
addMessage('assistant', WELCOME_MESSAGE.content);
userInput.focus();