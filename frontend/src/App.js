import React, { useState, useRef, useEffect, useMemo } from 'react';
import './App.css';

function App() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [consultations, setConsultations] = useState(() => {
    const saved = localStorage.getItem('consultations');
    return saved ? JSON.parse(saved) : [];
  });
  const [activeConsultationId, setActiveConsultationId] = useState(() => {
    return localStorage.getItem('activeConsultationId') || null;
  });

  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedMessage, setExpandedMessage] = useState(null);

  const viewportRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Sync theme to localStorage
  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Sync consultations to localStorage
  useEffect(() => {
    localStorage.setItem('consultations', JSON.stringify(consultations));
  }, [consultations]);

  // Sync activeConsultationId to localStorage
  useEffect(() => {
    if (activeConsultationId) {
      localStorage.setItem('activeConsultationId', activeConsultationId);
    } else {
      localStorage.removeItem('activeConsultationId');
    }
  }, [activeConsultationId]);

  // Auto-scroll to bottom when messages change or typing starts
  const activeConsultation = consultations.find(c => c.id === activeConsultationId);
  const messages = useMemo(() => activeConsultation ? activeConsultation.messages : [], [activeConsultation]);

  useEffect(() => {
    if (viewportRef.current) {
      viewportRef.current.scrollTop = viewportRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const createNewConsultation = () => {
    const newId = Date.now().toString();
    const newConsultation = {
      id: newId,
      title: 'New Consultation',
      messages: [],
      timestamp: new Date().toISOString()
    };
    setConsultations(prev => [newConsultation, ...prev]);
    setActiveConsultationId(newId);
    setSidebarOpen(false);
  };

  const deleteConsultation = (e, id) => {
    e.stopPropagation();
    setConsultations(prev => prev.filter(c => c.id !== id));
    if (activeConsultationId === id) {
      setActiveConsultationId(null);
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setAttachedFiles(prev => [...prev, ...files]);
    e.target.value = '';
  };

  const removeAttachment = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSendMessage = async (textOverride = null) => {
    const messageText = textOverride || inputValue;
    if (!messageText.trim() && attachedFiles.length === 0) return;

    let currentConsultationId = activeConsultationId;
    let updatedConsultations = [...consultations];

    // If no active consultation, create one
    if (!currentConsultationId) {
      const newId = Date.now().toString();
      const newConsultation = {
        id: newId,
        title: messageText.slice(0, 30) + (messageText.length > 30 ? '...' : ''),
        messages: [],
        timestamp: new Date().toISOString()
      };
      updatedConsultations = [newConsultation, ...updatedConsultations];
      currentConsultationId = newId;
      setConsultations(updatedConsultations);
      setActiveConsultationId(newId);
    }

    const userMessage = {
      id: Date.now(),
      text: messageText,
      role: 'user',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      files: [...attachedFiles]
    };

    // Update messages for the current consultation
    setConsultations(prev => prev.map(c => {
      if (c.id === currentConsultationId) {
        const isFirstMessage = c.messages.length === 0;
        return {
          ...c,
          title: isFirstMessage ? (messageText.slice(0, 30) + (messageText.length > 30 ? '...' : '')) : c.title,
          messages: [...c.messages, userMessage]
        };
      }
      return c;
    }));

    setInputValue('');
    setAttachedFiles([]);
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: messageText })
      });

      if (!response.ok) {
        throw new Error('API response error');
      }

      const data = await response.json();
      setIsTyping(false);

      const aiResponse = formatBackendResponse(data);
      const aiMessage = {
        id: Date.now() + 1,
        text: aiResponse,
        role: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        data: data
      };

      setConsultations(prev => prev.map(c => {
        if (c.id === currentConsultationId) {
          return {
            ...c,
            messages: [...c.messages, aiMessage]
          };
        }
        return c;
      }));

    } catch (error) {
      setIsTyping(false);
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: `Error: Unable to connect to backend. ${error.message}`,
        role: 'ai',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setConsultations(prev => prev.map(c => {
        if (c.id === currentConsultationId) {
          return {
            ...c,
            messages: [...c.messages, errorMessage]
          };
        }
        return c;
      }));
    }
  };

  const formatBackendResponse = (data) => {
    const { category, confidence, legal_frameworks, laws, steps, resources, warnings, context } = data;

    let response = `### 📋 LEGAL PRELIMINARY REPORT\n\n`;

    // Header Section
    response += `#### 🏷️ CASE SUMMARY\n`;
    response += `* **Primary Category:** ${category.replace(/_/g, ' ').toUpperCase()}\n`;
    response += `* **Confidence Level:** ${(confidence * 100).toFixed(1)}%\n`;

    if (context && context.authority) {
      response += `* **Involved Party Type:** ${context.authority.replace(/_/g, ' ')}\n`;
    }

    // POCSO/Emergency Notice
    if (context && context.legal_framework === 'POCSO' && context.age_indicator) {
      response += `\n> ⚠️ **CRITICAL PROTECTION NOTICE**: This case involves a minor. The **Protection of Children from Sexual Offences (POCSO) Act, 2012** is applicable, providing strict anonymity and special legal procedures.\n`;
    }

    // Legal Frameworks & Laws
    if ((legal_frameworks && legal_frameworks.length > 0) || (laws && laws.length > 0)) {
      response += `\n#### ⚖️ STATUTORY FRAMEWORK\n`;

      if (legal_frameworks && legal_frameworks.length > 0) {
        response += `**Governing Acts:**\n`;
        legal_frameworks.forEach(fw => response += `* ${fw}\n`);
      }

      if (laws && laws.length > 0) {
        response += `\n**Key Legal Provisions:**\n`;
        laws.slice(0, 5).forEach(law => {
          response += `* **Section ${law.section}** (${law.act}): ${law.title}\n`;
        });
      }
    }

    // Procedural Steps
    if (steps && steps.length > 0) {
      response += `\n#### � ACTIONABLE PROCEDURES\n`;
      steps.slice(0, 8).forEach((step, idx) => {
        response += `${idx + 1}. ${step}\n`;
      });
    }

    // Warnings & Support
    if (warnings && warnings.length > 0) {
      response += `\n#### ⚠️ IMPORTANT ADVISORIES\n`;
      warnings.forEach(warning => response += `* ${warning}\n`);
    }

    if (resources && resources.length > 0) {
      response += `\n#### 📞 CONTACT & SUPPORT\n`;
      resources.slice(0, 4).forEach(res => {
        const resText = typeof res === 'string' ? res : (res.name || res);
        response += `* ${resText}\n`;
      });
    }

    response += `\n---\n**PROVISIONAL NEXT STEPS**: You are advised to consult with a registered legal practitioner or visit the nearest police station for formal proceedings.`;
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
                {file.type?.startsWith('image/') ? (
                  <img src={URL.createObjectURL(file)} alt="upload" style={{ maxWidth: '100%', borderRadius: '8px' }} />
                ) : (
                  <div className="file-box" style={{ padding: '10px', background: 'rgba(0,0,0,0.05)', borderRadius: '8px', fontSize: '14px' }}>📄 {file.name}</div>
                )}
              </div>
            ))}
            {msg.text && (
              <div className="text structured-response">
                {msg.text.split('\n').map((line, i) => {
                  if (line.startsWith('### ')) {
                    return <h3 key={i} className="res-h3">{line.replace('### ', '')}</h3>;
                  }
                  if (line.startsWith('#### ')) {
                    return <h4 key={i} className="res-h4">{line.replace('#### ', '')}</h4>;
                  }
                  if (line.startsWith('> ')) {
                    return <blockquote key={i} className="res-quote">{line.replace('> ', '')}</blockquote>;
                  }
                  if (line.startsWith('* ')) {
                    return <div key={i} className="res-list-item"><span>•</span> {line.replace('* ', '')}</div>;
                  }
                  if (/^\d+\. /.test(line)) {
                    return <div key={i} className="res-step-item">{line}</div>;
                  }
                  if (line === '---') {
                    return <hr key={i} className="res-divider" />;
                  }
                  return <p key={i} style={{ marginBottom: '8px' }}>{line}</p>;
                })}
              </div>
            )}
          </div>
          <div className="msg-info">
            {msg.role === 'ai' ? 'Juris Guide' : 'You'} • {msg.time}
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
              <span className="logo-text">Juris Guide</span>
            </div>
            <button className="mobile-close" onClick={() => setSidebarOpen(false)}>×</button>
          </div>

          <button className="new-chat-btn" onClick={createNewConsultation}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
            New Consultation
          </button>

          <nav className="sidebar-nav">
            <div className="nav-section">
              <span className="section-title">Recent Conversations</span>
              <ul className="chat-history">
                {consultations.length === 0 ? (
                  <li className="history-item empty" style={{ fontStyle: 'italic', fontSize: '0.8rem', opacity: 0.6 }}>No recent chats</li>
                ) : (
                  consultations.map(chat => (
                    <li
                      key={chat.id}
                      className={`history-item ${activeConsultationId === chat.id ? 'active' : ''}`}
                      onClick={() => {
                        setActiveConsultationId(chat.id);
                        setSidebarOpen(false);
                      }}
                    >
                      <span className="history-icon">💬</span>
                      <span className="history-label" style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {chat.title}
                      </span>
                      <button
                        className="delete-chat"
                        onClick={(e) => deleteConsultation(e, chat.id)}
                        style={{ opacity: 0.4, fontSize: '14px' }}
                      >
                        ×
                      </button>
                    </li>
                  ))
                )}
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
                <h2>{activeConsultation ? activeConsultation.title : 'Juris Guide'}</h2>
                <span className="status-indicator">● Online</span>
              </div>
            </div>

            <div className="header-actions">
              <button className="theme-toggle-btn" onClick={toggleTheme} title="Change Theme">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle cx="12" cy="12" r="3" /></svg>
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
                  <div className="suggestion-card" onClick={() => handleSendMessage('Review the attached NDA for risks.')}>
                    <span className="card-icon">📄</span>
                    <h3>Review Contract</h3>
                    <p>Identify risks in NDAs or lease agreements.</p>
                  </div>
                  <div className="suggestion-card" onClick={() => handleSendMessage('What are the latest precedents on intellectual property rights?')}>
                    <span className="card-icon">🏛️</span>
                    <h3>Legal Research</h3>
                    <p>Query specific case laws or statutes.</p>
                  </div>
                  <div className="suggestion-card" onClick={() => handleSendMessage('Draft a formal notice for a tenant dispute.')}>
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
                      {file.type?.startsWith('image/') ? (
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
                  onClick={() => handleSendMessage()}
                  disabled={!inputValue.trim() && attachedFiles.length === 0}
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                </button>
              </div>
            </div>
            <p className="disclaimer">Juris Guide is an AI assistant and does not provide binding legal advice.</p>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
