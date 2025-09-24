// Obtiene los elementos principales del DOM
const chatMessages = document.querySelector(".chat-messages");
const messageInput = document.querySelector(".chat-input-area input");
const sendButton = document.querySelector(".chat-input-area button");
const chatItems = document.querySelectorAll(".chat-item");
const chatSearchInput = document.querySelector(".chat-search input");
const chatActionsButton = document.querySelector(".chat-actions .fa-ellipsis-v");

const conversations = {
    'Helena Hills': [
        { text: 'Hola, ¿qué tal?', sent: false },
        { text: 'Todo bien, gracias. ¿Y tú?', sent: true },
        { text: 'Will head to the Help Center...', sent: false }
    ],
    'Carlo Emilie': [
        { text: '¡Hey! ¿Listo para el proyecto?', sent: false },
        { text: '¡Claro! Let\'s go!', sent: true }
    ],
    'Oscar Davis': [
        { text: '¡Hola! Me podrías ayudar a crear un post para mi nueva adquisición?', sent: false },
        { text: 'Claro, ¿tienes alguna idea en mente?', sent: true },
        { text: 'Sí, estoy pensando en un post de un auto clásico.', sent: false }
    ]
};

function createMessageElement(messageText, isSent = true) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(isSent ? "sent" : "received");

    const messageParagraph = document.createElement("p");
    messageParagraph.textContent = messageText;
    
    const messageTime = document.createElement("span");
    const now = new Date();
    messageTime.textContent = `${now.getHours()}:${now.getMinutes()}`;
    
    messageDiv.appendChild(messageParagraph);
    messageDiv.appendChild(messageTime);

    return messageDiv;
}

function loadConversation(userName) {
    chatMessages.innerHTML = '';
    const chatHistory = conversations[userName] || [];
    chatHistory.forEach(msg => {
        const messageElement = createMessageElement(msg.text, msg.sent);
        chatMessages.appendChild(messageElement);
    });
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const messageText = messageInput.value.trim();
    if (messageText !== "") {
        const newMessage = createMessageElement(messageText, true);
        chatMessages.appendChild(newMessage);
        messageInput.value = "";
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

function filterChats() {
    const searchTerm = chatSearchInput.value.toLowerCase();
    chatItems.forEach(item => {
        const chatName = item.querySelector("h5").textContent.toLowerCase();
        if (chatName.includes(searchTerm)) {
            item.style.display = "flex";
        } else {
            item.style.display = "none";
        }
    });
}

function toggleProfileMenu() {
    let profileMenu = document.querySelector('.profile-menu');
    if (!profileMenu) {
        profileMenu = document.createElement('div');
        profileMenu.classList.add('profile-menu');
        profileMenu.innerHTML = `
            <ul>
                <li>Revisar perfil</li>
                <li>Reportar</li>
            </ul>
        `;
        document.body.appendChild(profileMenu);
        
        const buttonRect = chatActionsButton.getBoundingClientRect();
        profileMenu.style.top = `${buttonRect.bottom + 5}px`;
        profileMenu.style.right = `${window.innerWidth - buttonRect.right}px`;
        profileMenu.style.display = 'block';

        document.addEventListener('click', (event) => {
            if (!chatActionsButton.contains(event.target) && !profileMenu.contains(event.target)) {
                profileMenu.style.display = 'none';
            }
        });

    } else {
        profileMenu.style.display = profileMenu.style.display === 'block' ? 'none' : 'block';
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const initialChat = document.querySelector(".chat-item.active");
    if (initialChat) {
        const initialUser = initialChat.querySelector("h5").textContent;
        loadConversation(initialUser);
    }
});

chatItems.forEach(item => {
    item.addEventListener("click", () => {
        chatItems.forEach(chat => chat.classList.remove("active"));
        item.classList.add("active");
        const userName = item.querySelector("h5").textContent;
        loadConversation(userName);
    });
});

if (sendButton) {
    sendButton.addEventListener("click", sendMessage);
}

if (messageInput) {
    messageInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}

if (chatSearchInput) {
    chatSearchInput.addEventListener("keyup", filterChats);
}

if (chatActionsButton) {
    chatActionsButton.addEventListener("click", toggleProfileMenu);
}