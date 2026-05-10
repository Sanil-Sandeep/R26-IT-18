import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import MessageBubble from './components/MessageBubble';
import LoginQuiz from './components/LoginQuiz';
import TeacherDashboard from './components/TeacherDashboard';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [studentId, setStudentId]         = useState(null);
  const [studentName, setStudentName]     = useState('');
  const [nameInput, setNameInput]         = useState('');
  const [nameError, setNameError]         = useState('');
  const [messages, setMessages]           = useState([]);
  const [inputText, setInputText]         = useState('');
  const [isLoading, setIsLoading]         = useState(false);
  const [emotionState, setEmotionState]   = useState('neutral');
  const [topics, setTopics]               = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [loginQuiz, setLoginQuiz]         = useState(null);
  const [showQuiz, setShowQuiz]           = useState(false);
  const [showTeacher, setShowTeacher]     = useState(false);
  const [serverOnline, setServerOnline]   = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const savedName = localStorage.getItem('ict_student_name');
    const savedId   = localStorage.getItem('ict_student_id');
    if (savedName && savedId) {
      setStudentName(savedName);
      setStudentId(savedId);
    }
  }, []);

  useEffect(() => {
    if (studentId) {
      checkServer();
      loadTopics();
      checkLoginQuiz(studentId);
    }
  }, [studentId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleLogin = () => {
    const name = nameInput.trim();
    if (!name) { setNameError('Please enter your name.'); return; }
    if (name.length < 2) { setNameError('Name must be at least 2 characters.'); return; }
    const uniqueId = `student_${name.toLowerCase().replace(/\s+/g, '_')}_${Date.now()}`;
    localStorage.setItem('ict_student_name', name);
    localStorage.setItem('ict_student_id', uniqueId);
    setStudentName(name);
    setStudentId(uniqueId);
    setNameError('');
  };

  const handleLogout = () => {
    localStorage.removeItem('ict_student_name');
    localStorage.removeItem('ict_student_id');
    setStudentId(null); setStudentName(''); setNameInput('');
    setMessages([]); setShowQuiz(false); setLoginQuiz(null);
  };

  const checkServer = async () => {
    try {
      const r = await axios.get(`${API_URL}/health`);
      setServerOnline(r.data.chatbot_ready);
    } catch { setServerOnline(false); }
  };

  const loadTopics = async () => {
    try {
      const r = await axios.get(`${API_URL}/topics`);
      if (r.data.success) setTopics(r.data.topics);
    } catch (e) { console.error(e); }
  };

  const checkLoginQuiz = async (sid) => {
    try {
      const r = await axios.get(`${API_URL}/quiz/login?student_id=${sid}`);
      if (r.data.success && r.data.has_quiz) { setLoginQuiz(r.data.quiz); setShowQuiz(true); }
    } catch (e) { console.error(e); }
  };

  const sendMessage = async () => {
    const text = inputText.trim();
    if (!text || isLoading) return;
    setMessages(prev => [...prev, { id: Date.now(), role: 'student', text, timestamp: new Date().toISOString() }]);
    setInputText(''); setIsLoading(true);
    try {
      const r = await axios.post(`${API_URL}/chat`, {
        message: text, student_id: studentId,
        emotion_state: emotionState === 'neutral' ? null : emotionState
      });
      const d = r.data;
      setMessages(prev => [...prev, {
        id: Date.now() + 1, role: 'chatbot', text: d.message,
        intent: d.intent, emotion_detected: d.emotion_detected,
        topic: d.topic, confidence: d.confidence || 0,
        found_answer: d.found_answer, visual_suggestion: d.visual_suggestion,
        alert_message: d.alert_message, re_entry_message: d.re_entry_message,
        difficulty_message: d.difficulty_message,
        timestamp: d.timestamp || new Date().toISOString()
      }]);
    } catch {
      setMessages(prev => [...prev, {
        id: Date.now() + 1, role: 'chatbot',
        text: '❌ Cannot connect to server. Make sure Flask is running.',
        timestamp: new Date().toISOString(), confidence: 0, found_answer: false
      }]);
    }
    setIsLoading(false);
  };

  const handleKeyDown = (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } };

  const emotions = [
    { key: 'neutral', label: '😐 Neutral' }, { key: 'confused', label: '😕 Confused' },
    { key: 'bored', label: '😴 Bored' }, { key: 'distracted', label: '😵 Distracted' },
    { key: 'understanding', label: '😊 Understanding' },
  ];

  const suggestions = ['What is ICT?','Define database','Explain how a network works','What is a CPU?','List types of software','What is normalization?'];

  if (!studentId) {
    return (
      <div className="login-screen">
        <div className="login-box">
          <div className="login-emoji">🤖</div>
          <h1>ICT Learning Assistant</h1>
          <p>O/L Information Technology Chatbot</p>
          <div className="login-form">
            <label>Enter your name to start learning:</label>
            <input className="login-input" type="text" placeholder="e.g. Sanil, Amal, Nimal..."
              value={nameInput} onChange={(e) => { setNameInput(e.target.value); setNameError(''); }}
              onKeyDown={(e) => e.key === 'Enter' && handleLogin()} autoFocus />
            {nameError && <p className="login-error">{nameError}</p>}
            <button className="login-btn" onClick={handleLogin}>Start Learning 🚀</button>
          </div>
          <p className="login-note">💡 Each student gets their own learning session and quiz history.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="header">
        <div className="header-left">
          <div className="header-avatar">🤖</div>
          <div className="header-info">
            <h1>ICT Learning Assistant</h1>
            <p>Hello, {studentName}! 👋 Ready to learn?</p>
          </div>
        </div>
        <div className="header-right">
          <div className="status-dot" title={serverOnline ? 'Online' : 'Offline'} />
          <button className="teacher-btn" onClick={() => setShowTeacher(true)}>👨‍🏫 Teacher View</button>
          <button className="teacher-btn" onClick={handleLogout}>🔄 Logout</button>
        </div>
      </div>

      <div className="emotion-bar">
        <span>How are you feeling?</span>
        <span className={`emotion-badge emotion-${emotionState}`}>
          {emotions.find(e => e.key === emotionState)?.label}
        </span>
        <span style={{ fontSize: '11px', color: '#a0aec0' }}>(This changes how I explain things)</span>
      </div>

      {topics.length > 0 && (
        <div className="topic-bar">
          <span>Topics:</span>
          <button className={`topic-chip ${!selectedTopic ? 'active' : ''}`} onClick={() => setSelectedTopic(null)}>All</button>
          {topics.map(t => (
            <button key={t} className={`topic-chip ${selectedTopic === t ? 'active' : ''}`} onClick={() => setSelectedTopic(t)}>{t}</button>
          ))}
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-emoji">🤖</div>
            <h2>Hello, {studentName}! I'm your ICT Assistant</h2>
            <p>Ask me anything about O/L Information Technology.<br />I can explain concepts, give exam answers, and quiz you!</p>
            <div className="welcome-suggestions">
              {suggestions.map((s, i) => <button key={i} className="suggestion-chip" onClick={() => setInputText(s)}>{s}</button>)}
            </div>
          </div>
        )}
        {messages.map(m => <MessageBubble key={m.id} message={m} studentId={studentId} />)}
        {isLoading && (
          <div className="message-wrapper chatbot">
            <div className="message-avatar bot">🤖</div>
            <div className="typing-indicator">
              <div className="typing-dot" /><div className="typing-dot" /><div className="typing-dot" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <div className="emotion-selector">
          <span>Emotion:</span>
          {emotions.map(e => (
            <button key={e.key} className={`emotion-btn ${emotionState === e.key ? 'active' : ''}`} onClick={() => setEmotionState(e.key)}>{e.label}</button>
          ))}
        </div>
        <div className="input-row">
          <textarea className="message-input" placeholder="Ask me anything about ICT... (Press Enter to send)"
            value={inputText} onChange={(e) => setInputText(e.target.value)} onKeyDown={handleKeyDown} rows={1} />
          <button className="send-btn" onClick={sendMessage} disabled={isLoading || !inputText.trim()}>➤</button>
        </div>
      </div>

      {showQuiz && loginQuiz && <LoginQuiz quiz={loginQuiz} studentId={studentId} onClose={() => setShowQuiz(false)} />}
      {showTeacher && <TeacherDashboard onClose={() => setShowTeacher(false)} />}
    </div>
  );
}

export default App;
