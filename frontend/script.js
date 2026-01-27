/**
 * Judi Legal AI - Interaction Logic
 */

const state = {
    theme: localStorage.getItem('theme') || 'light',
    isTyping: false,
    attachedFiles: [],
    messages: []
};

// DOM Elements
const elements = {
    body: document.body,
    themeToggle: document.getElementById('themeToggle'),
    sidebar: document.getElementById('sidebar'),
    sidebarClose: document.getElementById('sidebarClose'),
    mobileToggle: document.getElementById('mobileToggle'),
    chatViewport: document.getElementById('chatViewport'),
    userInput: document.getElementById('userInput'),
    sendBtn: document.getElementById('sendBtn'),
    attachBtn: document.getElementById('attachBtn'),
    fileInput: document.getElementById('fileInput'),
    attachmentBar: document.getElementById('attachmentBar')
};

/**
 * Theme Management
 */
function initTheme() {
    elements.body.className = `${state.theme}-theme`;
}

function toggleTheme() {
    state.theme = state.theme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', state.theme);
    initTheme();
}

/**
 * Sidebar Management (Mobile)
 */
function toggleSidebar() {
    elements.sidebar.classList.toggle('open');
}

/**
 * Message Handling
 */
function addMessage(text, role, files = []) {
    // Hide welcome screen if it's the first message
    const welcomeScreen = document.querySelector('.welcome-screen');
    if (welcomeScreen) welcomeScreen.style.display = 'none';

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const messageId = Date.now();

    const messageHTML = `
        <div class="message ${role}" id="msg-${messageId}">
            <div class="msg-avatar">${role === 'ai' ? '⚖️' : '👤'}</div>
            <div class="msg-content">
                <div class="bubble">
                    ${files.length > 0 ? renderAttachments(files) : ''}
                    <div class="text">${escapeHtml(text)}</div>
                </div>
                <div class="msg-info">${role === 'ai' ? 'Judi' : 'You'} • ${time}</div>
            </div>
        </div>
    `;

    elements.chatViewport.insertAdjacentHTML('beforeend', messageHTML);
    scrollToBottom();
}

function renderAttachments(files) {
    return `
        <div class="message-attachments" style="display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;">
            ${files.map(file => {
        if (file.type.startsWith('image/')) {
            const url = URL.createObjectURL(file);
            return `<img src="${url}" style="max-width: 200px; border-radius: 8px; border: 1px solid rgba(0,0,0,0.1);">`;
        }
        return `<div style="padding: 8px 12px; background: rgba(0,0,0,0.05); border-radius: 6px; font-size: 0.8rem; display: flex; align-items: center; gap: 6px;">📄 ${file.name}</div>`;
    }).join('')}
        </div>
    `;
}

function showTypingIndicator() {
    const indicatorHTML = `
        <div class="message ai typing" id="typing-indicator">
            <div class="msg-avatar">⚖️</div>
            <div class="msg-content">
                <div class="bubble">
                    <div class="typing-dots">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        </div>
    `;
    elements.chatViewport.insertAdjacentHTML('beforeend', indicatorHTML);
    scrollToBottom();
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

async function handleSendMessage() {
    const text = elements.userInput.value.trim();
    const files = [...state.attachedFiles];

    if (!text && files.length === 0) return;

    // Clear input and attachments
    elements.userInput.value = '';
    elements.userInput.style.height = 'auto';
    state.attachedFiles = [];
    renderAttachmentBar();
    updateSendButton();

    // Add user message
    addMessage(text, 'user', files);

    // Simulate AI response
    showTypingIndicator();

    // Artificial delay to feel natural
    const delay = Math.random() * 1000 + 1500;
    setTimeout(() => {
        hideTypingIndicator();
        const response = getAIResponse(text);
        addMessage(response, 'ai');
    }, delay);
}

function getAIResponse(query) {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('contract')) {
        return "I can help you analyze the legal implications of this contract. Would you like me to look for specific clauses like 'termination', 'indemnity', or 'governing law'?";
    }
    if (lowerQuery.includes('hello') || lowerQuery.includes('hi')) {
        return "Greetings. I am Judi, your AI legal advisor. How may I assist you with your legal research or documentation today?";
    }
    if (lowerQuery.includes('divorce') || lowerQuery.includes('family')) {
        return "Family law matters are sensitive. While I can provide information on general procedures and common requirements, I recommend consulting with a family law specialist for your specific regional jurisdiction.";
    }

    const genericResponses = [
        "That's a complex legal question. Let me break down the standard legal framework for this situation...",
        "Based on common legal precedents, here is how such cases are typically handled...",
        "I've processed your query. To give you the most accurate guidance, I'll need to know which jurisdiction applies here.",
        "Under current statutes, this particular matter falls under civil liability. Let me explain the key elements required to prove such a claim."
    ];

    return genericResponses[Math.floor(Math.random() * genericResponses.length)];
}

/**
 * File Handling
 */
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    state.attachedFiles.push(...files);
    renderAttachmentBar();
    updateSendButton();
    e.target.value = ''; // Reset input
}

function renderAttachmentBar() {
    if (state.attachedFiles.length === 0) {
        elements.attachmentBar.innerHTML = '';
        return;
    }

    elements.attachmentBar.innerHTML = state.attachedFiles.map((file, index) => {
        const isImage = file.type.startsWith('image/');
        return `
            <div class="att-preview">
                ${isImage ? `<img src="${URL.createObjectURL(file)}">` : `<div style="height:100%; display:flex; align-items:center; justify-content:center; font-size:24px;">📄</div>`}
                <button class="att-remove" onclick="removeAttachment(${index})">×</button>
            </div>
        `;
    }).join('');
}

window.removeAttachment = (index) => {
    state.attachedFiles.splice(index, 1);
    renderAttachmentBar();
    updateSendButton();
};

/**
 * Utilities
 */
function scrollToBottom() {
    elements.chatViewport.scrollTop = elements.chatViewport.scrollHeight;
}

function updateSendButton() {
    elements.sendBtn.disabled = !elements.userInput.value.trim() && state.attachedFiles.length === 0;
}

function autoResizeTextarea() {
    elements.userInput.style.height = 'auto';
    elements.userInput.style.height = elements.userInput.scrollHeight + 'px';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Initialization
 */
function init() {
    initTheme();

    // Event Listeners
    elements.themeToggle.addEventListener('click', toggleTheme);
    elements.mobileToggle.addEventListener('click', toggleSidebar);
    elements.sidebarClose.addEventListener('click', toggleSidebar);

    elements.sendBtn.addEventListener('click', handleSendMessage);
    elements.userInput.addEventListener('input', () => {
        autoResizeTextarea();
        updateSendButton();
    });

    elements.userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    elements.attachBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Initial focus
    elements.userInput.focus();
}

document.addEventListener('DOMContentLoaded', init);
