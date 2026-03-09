import React, { useState, useRef, useEffect, useMemo } from 'react';
import './App.css';

function App() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

  // Consultations are stored per-user under key `consultations_<username>`.
  const [consultations, setConsultations] = useState(() => {
    try {
      const savedUser = localStorage.getItem('user');
      const username = savedUser ? JSON.parse(savedUser).username : null;
      const key = username ? `consultations_${username}` : 'consultations';
      const saved = localStorage.getItem(key);
      return saved ? JSON.parse(saved) : [];
    } catch (err) {
      return [];
    }
  });

  const [activeConsultationId, setActiveConsultationId] = useState(() => {
    try {
      const savedUser = localStorage.getItem('user');
      const username = savedUser ? JSON.parse(savedUser).username : null;
      const key = username ? `activeConsultationId_${username}` : 'activeConsultationId';
      return localStorage.getItem(key) || null;
    } catch (err) {
      return null;
    }
  });

  const [isTyping, setIsTyping] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [attachedFiles, setAttachedFiles] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [expandedMessage, setExpandedMessage] = useState(null);

  // Location selector state (used to show local resource numbers)
  const [locations, setLocations] = useState(['National']);
  const [selectedLocation, setSelectedLocation] = useState(localStorage.getItem('selectedLocation') || 'National');

  // User / Login state
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isSignup, setIsSignup] = useState(false);

  const viewportRef = useRef(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  // Sync theme to localStorage
  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  // Sync consultations to per-user localStorage key
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('user');
      const username = savedUser ? JSON.parse(savedUser).username : null;
      const key = username ? `consultations_${username}` : 'consultations';
      localStorage.setItem(key, JSON.stringify(consultations));
    } catch (err) {
      // ignore
    }
  }, [consultations]);

  // Sync consultations to backend for the logged-in user
  useEffect(() => {
    const saveToServer = async () => {
      try {
        const savedUser = localStorage.getItem('user');
        const username = savedUser ? JSON.parse(savedUser).username : null;
        if (!username) return;
        await fetch(`http://localhost:8000/consultations/${encodeURIComponent(username)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ consultations, activeConsultationId })
        });
      } catch (err) {
        // ignore server save errors for now
      }
    };
    saveToServer();
  }, [consultations, activeConsultationId, user]);

  // Sync activeConsultationId to per-user localStorage key
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('user');
      const username = savedUser ? JSON.parse(savedUser).username : null;
      const key = username ? `activeConsultationId_${username}` : 'activeConsultationId';
      if (activeConsultationId) {
        localStorage.setItem(key, activeConsultationId);
      } else {
        localStorage.removeItem(key);
      }
    } catch (err) {
      // ignore
    }
  }, [activeConsultationId]);

  // When the logged-in user changes, load their consultations
  useEffect(() => {
    try {
      const savedUser = localStorage.getItem('user');
      const username = savedUser ? JSON.parse(savedUser).username : null;
      const consultKey = username ? `consultations_${username}` : 'consultations';
      const activeKey = username ? `activeConsultationId_${username}` : 'activeConsultationId';
      const savedConsults = localStorage.getItem(consultKey);
      setConsultations(savedConsults ? JSON.parse(savedConsults) : []);
      const savedActive = localStorage.getItem(activeKey);
      setActiveConsultationId(savedActive || null);
    } catch (err) {
      setConsultations([]);
      setActiveConsultationId(null);
    }
  }, [/* run when `user` changes */ user]);

  // fetch available locations (read from backend) and persist selection
  useEffect(() => {
    const fetchLocations = async () => {
      try {
        const res = await fetch('http://localhost:8000/locations');
        if (!res.ok) return;
        const payload = await res.json();
        if (payload && Array.isArray(payload.locations)) {
          setLocations(payload.locations);
          const stored = localStorage.getItem('selectedLocation') || 'National';
          if (!payload.locations.includes(stored)) {
            const pick = payload.locations[0] || 'National';
            setSelectedLocation(pick);
            localStorage.setItem('selectedLocation', pick);
          }
        }
      } catch (err) {
        // ignore network errors
      }
    };
    fetchLocations();
  }, []);

  // persist selected location to localStorage
  useEffect(() => {
    localStorage.setItem('selectedLocation', selectedLocation);
  }, [selectedLocation]);

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
        body: JSON.stringify({ message: messageText, location: selectedLocation === 'National' ? null : selectedLocation })
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
    const { category, matched_categories, legal_frameworks, laws, steps, resources, warnings, context } = data;

    let response = `### 📋 LEGAL PRELIMINARY REPORT\n\n`;

    // Header Section
    response += `#### 🏷️ CASE SUMMARY\n`;
    if (matched_categories && matched_categories.length > 0) {
      const categoriesList = matched_categories.map(c => c.category.replace(/_/g, ' ').toUpperCase()).join(', ');
      response += `* **Categories:** ${categoriesList}\n`;
    } else {
      response += `* **Category:** ${category.replace(/_/g, ' ').toUpperCase()}\n`;
    }

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
          const sectionPart = law.section ? `**Section ${law.section}** ` : '';
          const actPart = law.act ? `(${law.act})` : '';
          const titlePart = law.title ? `: ${law.title}` : '';
          
          if (sectionPart || actPart || titlePart) {
            response += `* ${sectionPart}${actPart}${titlePart}\n`;
          } else {
            // Unlikely fallback if law is just a string or completely empty object
            response += `* ${JSON.stringify(law)}\n`;
          }
        });
      }
    }

    // Procedural Steps
    if (steps && steps.length > 0) {
      response += `\n#### 📝 ACTIONABLE PROCEDURES\n`;
      steps.forEach((step, idx) => {
        response += `${idx + 1}. ${step}\n`;
      });
    }

    // Warnings & Support
    if (warnings && warnings.length > 0) {
      response += `\n#### ⚠️ IMPORTANT ADVISORIES\n`;
      warnings.forEach(warning => response += `* ${warning}\n`);
    }

    const validResources = (resources || []).filter(res => {
      if (!res) return false;
      if (typeof res === 'string') return res.trim() !== '';
      if (typeof res === 'object') return res.name || res.location || res.description || res.contact || res.link;
      return false;
    });

    if (validResources.length > 0) {
      response += `\n#### 📞 CONTACT & SUPPORT\n`;
      validResources.forEach(res => {
        if (typeof res === 'string') {
          response += `* ${res}\n`;
        } else if (typeof res === 'object') {
          response += `* ${res.name || 'Resource'}\n`;
          if (res.location) response += `  📍 ${res.location}\n`;
          if (res.description) response += `  ℹ️ ${res.description}\n`;
          if (res.contact) response += `  ☎️ ${res.contact}\n`;
          if (res.link) response += `  🔗 ${res.link}\n`;
          response += `\n`;
        }
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

  const handleLogin = async () => {
    setIsLoggingIn(true);
    setLoginError(null);
    try {
      const endpoint = isSignup ? 'http://localhost:8000/signup' : 'http://localhost:8000/login';
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginUsername, password: loginPassword })
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || data.error || 'Login failed');
      }
      const userObj = { username: data.user };
      setUser(userObj);
      localStorage.setItem('user', JSON.stringify(userObj));
      // Load consultations for this user from backend
      try {
        const resp = await fetch(`http://localhost:8000/consultations/${encodeURIComponent(userObj.username)}`);
        if (resp.ok) {
          const cdata = await resp.json();
          if (cdata && Array.isArray(cdata.consultations)) {
            setConsultations(cdata.consultations);
            setActiveConsultationId(cdata.activeConsultationId || null);
          }
        }
      } catch (err) {
        // ignore load errors
      }
    } catch (err) {
      setLoginError(err.message || 'Login failed');
    }
    setIsLoggingIn(false);
  };

  const handleLogout = () => {
    // Clear UI state but keep stored consultations for the user in localStorage
    setUser(null);
    localStorage.removeItem('user');
    setConsultations([]);
    setActiveConsultationId(null);
  };

  const renderMessage = (msg) => {
    const renderTextWithLinks = (text) => {
      const urlRegex = /(https?:\/\/[^\s]+)/g;
      if (!urlRegex.test(text)) return text;
      const parts = text.split(urlRegex);
      return parts.map((part, index) => {
        if (part.match(urlRegex)) {
          return (
            <a key={index} href={part} target="_blank" rel="noopener noreferrer" style={{ color: '#007BFF', textDecoration: 'underline' }}>
              {part}
            </a>
          );
        }
        return part;
      });
    };

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
                    return <h3 key={i} className="res-h3">{renderTextWithLinks(line.replace('### ', ''))}</h3>;
                  }
                  if (line.startsWith('#### ')) {
                    return <h4 key={i} className="res-h4">{renderTextWithLinks(line.replace('#### ', ''))}</h4>;
                  }
                  if (line.startsWith('> ')) {
                    return <blockquote key={i} className="res-quote">{renderTextWithLinks(line.replace('> ', ''))}</blockquote>;
                  }
                  if (line.startsWith('* ')) {
                    return <div key={i} className="res-list-item"><span>•</span> {renderTextWithLinks(line.replace('* ', ''))}</div>;
                  }
                  if (line.startsWith('  ')) {
                    return <div key={i} style={{ paddingLeft: '20px', marginBottom: '4px' }}>{renderTextWithLinks(line.trim())}</div>;
                  }
                  if (/^\d+\. /.test(line)) {
                    return <div key={i} className="res-step-item">{renderTextWithLinks(line)}</div>;
                  }
                  if (line === '---') {
                    return <hr key={i} className="res-divider" />;
                  }
                  if (line.trim() === '') {
                    return <div key={i} style={{ marginBottom: '8px' }}></div>;
                  }
                  return <p key={i} style={{ marginBottom: '8px' }}>{renderTextWithLinks(line)}</p>;
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

  if (!user) {
    return (
      <div className={`App ${theme}-theme`}>
        <div className="auth-wrapper">
          <div className="auth-card">
            <div className="auth-header">
              <h2>{isSignup ? 'Create an account' : 'Login to Judi'}</h2>
              <div className="auth-sub">Securely access your consultations and history.</div>
            </div>

            <div className="auth-field">
              <label>Username</label>
              <input className="auth-input" value={loginUsername} onChange={(e) => setLoginUsername(e.target.value)} />
            </div>

            <div className="auth-field">
              <label>Password</label>
              <input className="auth-input" type="password" value={loginPassword} onChange={(e) => setLoginPassword(e.target.value)} />
            </div>

            <div className="auth-actions">
              <button className="auth-btn auth-btn-primary" onClick={handleLogin} disabled={isLoggingIn || !loginUsername.trim() || !loginPassword}>{isLoggingIn ? (isSignup ? 'Creating...' : 'Logging in...') : (isSignup ? 'Sign up' : 'Login')}</button>
              <button className="auth-btn auth-btn-ghost" onClick={() => { setLoginUsername(''); setLoginPassword(''); setLoginError(null); }}>Clear</button>
            </div>

            <div className="auth-toggle">
              <div className="auth-small-note">{isSignup ? 'Already have an account?' : "Don't have an account?"}</div>
              <button onClick={() => { setIsSignup(prev => !prev); setLoginError(null); }} style={{ background: 'transparent', border: 'none', color: 'var(--accent-color)', cursor: 'pointer' }}>{isSignup ? 'Login' : 'Create account'}</button>
            </div>

            {loginError && <div className="auth-error">{loginError}</div>}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`App ${theme}-theme`}>
      <div className="app-container">
        {/* Sidebar */}
        <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
          <div className="sidebar-header">
            <div className="logo">
              <div className="logo-icon">⚖️</div>
              <span className="logo-text">Judi</span>
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
                <h2>{activeConsultation ? activeConsultation.title : 'Judi'}</h2>
                <span className="status-indicator">● Online</span>
              </div>
            </div>

            <div className="header-actions">
              <select
                className="location-select"
                value={selectedLocation}
                onChange={(e) => setSelectedLocation(e.target.value)}
                title="Select location for local resources"
                aria-label="Location selector"
              >
                {locations.map(loc => <option key={loc} value={loc}>{loc}</option>)}
              </select>
              <button className="theme-toggle-btn" onClick={toggleTheme} title="Change Theme">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle cx="12" cy="12" r="3" /></svg>
              </button>
              {user && (
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: '10px', marginLeft: '12px' }}>
                  <div style={{ fontSize: '14px', color: '#333' }}>{user.username}</div>
                  <button onClick={handleLogout} title="Sign out" style={{ padding: '6px 10px', borderRadius: 6, border: '1px solid rgba(0,0,0,0.08)', background: 'transparent', cursor: 'pointer' }}>Logout</button>
                </div>
              )}
            </div>
          </header>

          <div className="chat-viewport" ref={viewportRef}>
            {messages.length === 0 && (
              <div className="welcome-screen">
                <div className="hero-logo">⚖️</div>
                <h1 className="hero-title">How can I assist your legal research today?</h1>
                <p className="hero-subtitle">Upload documents or ask complex legal questions to get started.</p>
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
            <p className="disclaimer">Judi is an AI assistant and does not provide binding legal advice.</p>
          </footer>
        </main>
      </div>
    </div>
  );
}

export default App;
