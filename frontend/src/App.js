import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedMessage, setExpandedMessage] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]);

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
    const messageToSend = inputValue;
    setInputValue('');
    setAttachedFiles([]);
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageToSend })
      });

      if (!response.ok) {
        throw new Error('API response error');
      }

      const data = await response.json();
      setIsTyping(false);

      // Format AI response from backend
      const aiResponse = formatBackendResponse(data);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: aiResponse,
        role: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        data: data  // Store full response data for reference
      }]);
    } catch (error) {
      setIsTyping(false);
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: `Error: Unable to connect to backend. ${error.message}`,
        role: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }
  };

  const formatBackendResponse = (data) => {
    const { category, confidence, matched_categories, legal_frameworks, laws, steps, resources, warnings, context } = data;
    
    let response = ``;
    
    // Primary Category with confidence
    response += `🏷️ **Case Category:** ${category.replace(/_/g, ' ').toUpperCase()}\n`;
    response += `📊 **Confidence:** ${(confidence * 100).toFixed(1)}%\n`;
    
    // Age-based POCSO notice
    if (context && context.legal_framework === 'POCSO' && context.age_indicator) {
      response += `\n⚠️ **IMPORTANT:** POCSO Framework Applicable - Minor victim detected. Additional protections under Protection of Children from Sexual Offences Act, 2012 apply.\n`;
    }
    
    // Matched Categories
    if (matched_categories && matched_categories.length > 1) {
      response += `\n🔍 **Other Possible Issues:**\n`;
      matched_categories.slice(1, 3).forEach(cat => {
        response += `   • ${cat.category.replace(/_/g, ' ')} (${(cat.confidence * 100).toFixed(1)}%)\n`;
      });
    }

    // Legal Frameworks
    if (legal_frameworks && legal_frameworks.length > 0) {
      response += `\n⚖️ **Applicable Legal Frameworks:**\n`;
      legal_frameworks.forEach(fw => {
        response += `   • ${fw}\n`;
      });
    }

    // Laws and Sections
    if (laws && laws.length > 0) {
      response += `\n📜 **Applicable Laws & Sections:**\n`;
      laws.slice(0, 5).forEach(law => {
        response += `   • **${law.section}** (${law.act}): ${law.title}\n`;
      });
      if (laws.length > 5) {
        response += `   ... and ${laws.length - 5} more laws\n`;
      }
    }

    // Procedural Steps
    if (steps && steps.length > 0) {
      response += `\n📋 **Steps to File Case (${steps.length} steps total):**\n`;
      steps.slice(0, 8).forEach((step, idx) => {
        response += `   ${idx + 1}. ${step}\n`;
      });
      if (steps.length > 8) {
        response += `   ... and ${steps.length - 8} more steps\n`;
      }
    }

    // Resources
    if (resources && resources.length > 0) {
      response += `\n📞 **Support Resources:**\n`;
      resources.slice(0, 4).forEach(res => {
        const resText = typeof res === 'string' ? res : (res.name || res);
        response += `   • ${resText}\n`;
      });
    }

    // Authority Context
    if (context && context.authority) {
      response += `\n👤 **Perpetrator Profile:** ${context.authority.replace(/_/g, ' ')}\n`;
    }

    // Warnings
    if (warnings && warnings.length > 0) {
      response += `\n⚠️ **Important Notes:**\n`;
      warnings.forEach(warning => {
        response += `   • ${warning}\n`;
      });
    }

    response += `\n✅ **Next Steps:** Contact local police station or legal aid organization for formal case filing.\n`;

    return response;
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleMessageExpand = (messageId) => {
    setExpandedMessage(expandedMessage === messageId ? null : messageId);
  };

  const renderMessage = (msg) => {
    return (
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
            {msg.text && (
              <div className="text">
                {msg.text.split('\n').map((line, i) => {
                  if (line.startsWith('   •')) {
                    return <div key={i} style={{ marginLeft: '20px', marginBottom: '4px' }}>{line}</div>;
                  }
                  if (line.startsWith('   ')) {
                    return <div key={i} style={{ marginLeft: '16px', marginBottom: '4px', fontFamily: 'monospace' }}>{line}</div>;
                  }
                  if (line.startsWith('**') && line.endsWith('**')) {
                    return <div key={i} style={{ fontWeight: 'bold', marginTop: '10px', marginBottom: '4px', fontSize: '0.95em' }}>{line}</div>;
                  }
                  return <div key={i} style={{ marginBottom: '2px' }}>{line}</div>;
                })}
              </div>
            )}
          </div>
          <div className="msg-info">
            {msg.role === 'ai' ? 'Judi' : 'You'} • {msg.time}
            {msg.data && msg.role === 'ai' && (
              <button 
                className="expand-btn"
                onClick={() => toggleMessageExpand(msg.id)}
                style={{ marginLeft: '10px', fontSize: '12px', color: '#666', cursor: 'pointer' }}
              >
                {expandedMessage === msg.id ? '▼ Hide Details' : '▶ Show Full Details'}
              </button>
            )}
          </div>
          {expandedMessage === msg.id && msg.data && (
            <div className="expanded-details" style={{ marginTop: '12px', padding: '12px', background: 'rgba(0,0,0,0.03)', borderRadius: '6px', fontSize: '13px' }}>
              {msg.data.laws && msg.data.laws.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <strong>📜 All Applicable Laws ({msg.data.laws.length}):</strong>
                  {msg.data.laws.map((law, idx) => (
                    <div key={idx} style={{ marginTop: '6px', paddingLeft: '12px', borderLeft: '2px solid #007BFF' }}>
                      <strong>Section {law.section}</strong> - {law.title}
                      <div style={{ fontSize: '12px', color: '#666', marginTop: '2px' }}>{law.description}</div>
                    </div>
                  ))}
                </div>
              )}
              {msg.data.steps && msg.data.steps.length > 0 && (
                <div style={{ marginBottom: '12px' }}>
                  <strong>📋 All Procedural Steps ({msg.data.steps.length}):</strong>
                  <ol style={{ marginTop: '6px', paddingLeft: '16px' }}>
                    {msg.data.steps.map((step, idx) => (
                      <li key={idx} style={{ marginTop: '4px' }}>{step}</li>
                    ))}
                  </ol>
                </div>
              )}
              {msg.data.case_references && msg.data.case_references.length > 0 && (
                <div>
                  <strong>🏛️ Relevant Case Laws:</strong>
                  {msg.data.case_references.slice(0, 3).map((caseRef, idx) => (
                    <div key={idx} style={{ marginTop: '4px', fontSize: '12px' }}>• {caseRef}</div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
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

            {messages.map(msg => renderMessage(msg))}

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
