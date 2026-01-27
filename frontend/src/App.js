import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const viewportRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    if (viewportRef.current) {
      viewportRef.current.scrollTop = viewportRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setAttachedFiles(prev => [...prev, ...files]);
    e.target.value = '';
  };

  const removeAttachment = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() && attachedFiles.length === 0) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      role: 'user',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      files: [...attachedFiles]
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setAttachedFiles([]);
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      setIsTyping(false);
      const aiResponse = getAIResponse(inputValue);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: aiResponse,
        role: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }, 1500 + Math.random() * 1000);
  };

  const getAIResponse = (query) => {
    const lowerQuery = query.toLowerCase();
    if (lowerQuery.includes('contract')) return "I can help you analyze the legal implications of this contract. Would you like me to look for specific clauses like 'termination' or 'governing law'?";
    if (lowerQuery.includes('hello') || lowerQuery.includes('hi')) return "Greetings. I am Judi, your AI legal advisor. How may I assist you with your legal research today?";

    const responses = [
      "That's a complex legal question. Let me break down the standard legal framework for this situation...",
      "Based on common legal precedents, here is how such cases are typically handled...",
      "Under current statutes, this particular matter falls under civil liability. Let me explain the key elements."
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={`App ${theme}-theme`}>
      <div className="app-container">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
          <div className="sidebar-header">
            <div className="logo">
              <div className="logo-icon">⚖️</div>
              <span className="logo-text">Consultant</span>
            </div>
            <button className="mobile-close" onClick={() => setSidebarOpen(false)}>×</button>
          </div>

          <button className="new-chat-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            New Consultation
          </button>

          <nav className="sidebar-nav">
            <div className="nav-section">
              <span className="section-title">Recent Conversations</span>
              <ul className="chat-history">
                <li className="history-item active">
                  <span className="history-icon">💬</span>
                  <span className="history-label">Employment Contract...</span>
                </li>
                <li className="history-item">
                  <span className="history-icon">💬</span>
                  <span className="history-label">IP Rights Advice</span>
                </li>
              </ul>
            </div>
          </nav>


        </aside>

        {/* Main Area */}
        <main className="main-content">
          <header className="top-header">
            <div className="header-left">
              <button className="mobile-toggle" onClick={() => setSidebarOpen(true)}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
              </button>
              <div className="current-chat-info">
                <h2>Legal Consultation</h2>
                <span className="status-indicator">● Online</span>
              </div>
            </div>

            <div className="header-actions">
              <button className="theme-toggle-btn" onClick={toggleTheme}>
                {theme === 'light' ? (
                  <svg className="moon-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
                ) : (
                  <svg className="sun-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
                )}
              </button>
            </div>
          </header>

          <div className="chat-viewport" ref={viewportRef}>
            {messages.length === 0 && (
              <div className="welcome-screen">
                <div className="hero-logo">⚖️</div>
                <h1 className="hero-title">How can I assist your legal research today?</h1>
                <p className="hero-subtitle">Upload documents or ask complex legal questions to get started.</p>
                <div className="suggestions-grid">
                  <div className="suggestion-card" onClick={() => setInputValue('Review the attached NDA for risks.')}>
                    <span className="card-icon">📄</span>
                    <h3>Review Contract</h3>
                    <p>Identify risks in NDAs or lease agreements.</p>
                  </div>
                  <div className="suggestion-card" onClick={() => setInputValue('What are the latest precedents on intellectual property rights?')}>
                    <span className="card-icon">🏛️</span>
                    <h3>Legal Research</h3>
                    <p>Query specific case laws or statutes.</p>
                  </div>
                  <div className="suggestion-card" onClick={() => setInputValue('Draft a formal notice for a tenant dispute.')}>
                    <span className="card-icon">✍️</span>
                    <h3>Draft Document</h3>
                    <p>Generate formal legal notices or letters.</p>
                  </div>
                </div>
              </div>
            )}

            {messages.map(msg => (
              <div key={msg.id} className={`message ${msg.role}`}>
                <div className="msg-avatar">{msg.role === 'ai' ? '⚖️' : '👤'}</div>
                <div className="msg-content">
                  <div className="bubble">
                    {msg.files && msg.files.map((file, i) => (
                      <div key={i} className="msg-attachment" style={{ marginBottom: msg.text ? '10px' : '0' }}>
                        {file.type.startsWith('image/') ? (
                          <img src={URL.createObjectURL(file)} alt="upload" style={{ maxWidth: '100%', borderRadius: '8px' }} />
                        ) : (
                          <div className="file-box" style={{ padding: '10px', background: 'rgba(0,0,0,0.05)', borderRadius: '8px', fontSize: '14px' }}>📄 {file.name}</div>
                        )}
                      </div>
                    ))}
                    {msg.text && <div className="text">{msg.text}</div>}
                  </div>
                  <div className="msg-info">{msg.role === 'ai' ? 'Judi' : 'You'} • {msg.time}</div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="message ai">
                <div className="msg-avatar">⚖️</div>
                <div className="msg-content">
                  <div className="bubble">
                    <div className="typing-dots">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <footer className="chat-footer">
            <div className="input-area-wrapper">
              {attachedFiles.length > 0 && (
                <div className="attachment-bar">
                  {attachedFiles.map((file, i) => (
                    <div key={i} className="att-preview">
                      {file.type.startsWith('image/') ? (
                        <img src={URL.createObjectURL(file)} alt="preview" />
                      ) : (
                        <div className="att-placeholder">📄</div>
                      )}
                      <button className="att-remove" onClick={() => removeAttachment(i)}>×</button>
                    </div>
                  ))}
                </div>
              )}

              <div className="input-container">
                <button className="attach-btn" onClick={() => fileInputRef.current.click()}>
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>
                </button>
                <input
                  type="file"
                  ref={fileInputRef}
                  hidden
                  multiple
                  onChange={handleFileChange}
                />

                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your legal query here..."
                  rows="1"
                />

                <button
                  className="send-btn"
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() && attachedFiles.length === 0}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
              </div>
            </div>
            <p className="disclaimer">Judi is an AI assistant and does not provide binding legal advice.</p>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
