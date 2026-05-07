/**
 * App.jsx
 * ========
 * Main React component - the complete chat interface.
 * 
 * This component handles:
 * - Sending messages to the Flask API
 * - Displaying chat messages
 * - Showing login quiz on startup
 * - Emotion selector
 * - Topic selector
 * - Teacher dashboard
 */

import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import MessageBubble from './components/MessageBubble';
import LoginQuiz from './components/LoginQuiz';
import TeacherDashboard from './components/TeacherDashboard';

const API_URL = 'http://localhost:5000/api';
const STUDENT_ID = 'student_1'; // In real system this comes from login

function App() {
  // ---- State Variables ----
  const [messages, setMessages] = useState([]);           // All chat messages
  const [inputText, setInputText] = useState('');         // Current input
  const [isLoading, setIsLoading] = useState(false);      // Loading indicator
  const [emotionState, setEmotionState] = useState('neutral'); // Selected emotion
  const [topics, setTopics] = useState([]);               // Available topics
  const [selectedTopic, setSelectedTopic] = useState(null); // Selected topic filter
  const [loginQuiz, setLoginQuiz] = useState(null);       // Login quiz data
  const [showQuiz, setShowQuiz] = useState(false);        // Show quiz modal
  const [showTeacher, setShowTeacher] = useState(false);  // Show teacher dashboard
  const [serverOnline, setServerOnline] = useState(false); // Server status

  // Ref to auto-scroll to bottom of chat
  const messagesEndRef = useRef(null);

  // ---- On App Load ----
  useEffect(() => {
    checkServer();
    loadTopics();
    checkLoginQuiz();
  }, []);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // ---- Check if server is running ----
  const checkServer = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`);
      setServerOnline(response.data.chatbot_ready);
    } catch {
      setServerOnline(false);
    }
  };

  // ---- Load available topics ----
  const loadTopics = async () => {
    try {
      const response = await axios.get(`${API_URL}/topics`);
      if (response.data.success) {
        setTopics(response.data.topics);
      }
    } catch (error) {
      console.error('Error loading topics:', error);
    }
  };

  // ---- Check if login quiz should be shown ----
  const checkLoginQuiz = async () => {
    try {
      const response = await axios.get(
        `${API_URL}/quiz/login?student_id=${STUDENT_ID}`
      );
      if (response.data.success && response.data.has_quiz) {
        setLoginQuiz(response.data.quiz);
        setShowQuiz(true);
      }
    } catch (error) {
      console.error('Error checking login quiz:', error);
    }
  };

  // ---- Send Message ----
  const sendMessage = async () => {
    const text = inputText.trim();
    if (!text || isLoading) return;

    // Add student message to chat
    const studentMessage = {
      id: Date.now(),
      role: 'student',
      text: text,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, studentMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Send to Flask API
      const response = await axios.post(`${API_URL}/chat`, {
        message: text,
        student_id: STUDENT_ID,
        emotion_state: emotionState === 'neutral' ? null : emotionState
      });

      const data = response.data;

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        role: 'chatbot',
        text: data.message,
        intent: data.intent,
        emotion_detected: data.emotion_detected,
        topic: data.topic,
        confidence: data.confidence || 0,
        found_answer: data.found_answer,
        visual_suggestion: data.visual_suggestion,
        alert_message: data.alert_message,
        re_entry_message: data.re_entry_message,
        difficulty_message: data.difficulty_message,
        timestamp: data.timestamp || new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      // Show error message if API fails
      const errorMessage = {
        id: Date.now() + 1,
        role: 'chatbot',
        text: '❌ Cannot connect to the chatbot server. Please make sure the Flask server is running.',
        timestamp: new Date().toISOString(),
        confidence: 0,
        found_answer: false
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  // ---- Handle Enter key ----
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // ---- Click suggestion chip ----
  const handleSuggestion = (text) => {
    setInputText(text);
  };

  // ---- Emotion options ----
  const emotions = [
    { key: 'neutral',       label: '😐 Neutral' },
    { key: 'confused',      label: '😕 Confused' },
    { key: 'bored',         label: '😴 Bored' },
    { key: 'distracted',    label: '😵 Distracted' },
    { key: 'understanding', label: '😊 Understanding' },
  ];

  // ---- Suggestion questions ----
  const suggestions = [
    'What is ICT?',
    'Define database',
    'Explain how a network works',
    'What is a CPU?',
    'List types of software',
    'What is normalization?',
  ];

  return (
    <div className="app">

      {/* ===================== HEADER ===================== */}
      <div className="header">
        <div className="header-left">
          <div className="header-avatar">🤖</div>
          <div className="header-info">
            <h1>ICT Learning Assistant</h1>
            <p>O/L Information Technology Chatbot</p>
          </div>
        </div>
        <div className="header-right">
          <div className="status-dot" title={serverOnline ? 'Online' : 'Offline'} />
          <button
            className="teacher-btn"
            onClick={() => setShowTeacher(true)}
          >
            👨‍🏫 Teacher View
          </button>
        </div>
      </div>

      {/* ===================== EMOTION BAR ===================== */}
      <div className="emotion-bar">
        <span>How are you feeling?</span>
        <span className={`emotion-badge emotion-${emotionState}`}>
          {emotions.find(e => e.key === emotionState)?.label || '😐 Neutral'}
        </span>
        <span style={{ fontSize: '11px', color: '#a0aec0' }}>
          (This changes how I explain things to you)
        </span>
      </div>

      {/* ===================== TOPIC BAR ===================== */}
      {topics.length > 0 && (
        <div className="topic-bar">
          <span>Topics:</span>
          <button
            className={`topic-chip ${!selectedTopic ? 'active' : ''}`}
            onClick={() => setSelectedTopic(null)}
          >
            All
          </button>
          {topics.map(topic => (
            <button
              key={topic}
              className={`topic-chip ${selectedTopic === topic ? 'active' : ''}`}
              onClick={() => setSelectedTopic(topic)}
            >
              {topic}
            </button>
          ))}
        </div>
      )}

      {/* ===================== CHAT MESSAGES ===================== */}
      <div className="chat-messages">

        {/* Welcome Screen (shown when no messages yet) */}
        {messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-emoji">🤖</div>
            <h2>Hello! I'm your ICT Learning Assistant</h2>
            <p>
              Ask me anything about O/L Information Technology.<br />
              I can explain concepts, give exam answers, and quiz you!
            </p>
            <div className="welcome-suggestions">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  className="suggestion-chip"
                  onClick={() => handleSuggestion(s)}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat Messages */}
        {messages.map(message => (
          <MessageBubble
            key={message.id}
            message={message}
            studentId={STUDENT_ID}
          />
        ))}

        {/* Typing Indicator */}
        {isLoading && (
          <div className="message-wrapper chatbot">
            <div className="message-avatar bot">🤖</div>
            <div className="typing-indicator">
              <div className="typing-dot" />
              <div className="typing-dot" />
              <div className="typing-dot" />
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* ===================== INPUT AREA ===================== */}
      <div className="input-area">

        {/* Emotion Selector */}
        <div className="emotion-selector">
          <span>Emotion:</span>
          {emotions.map(e => (
            <button
              key={e.key}
              className={`emotion-btn ${emotionState === e.key ? 'active' : ''}`}
              onClick={() => setEmotionState(e.key)}
            >
              {e.label}
            </button>
          ))}
        </div>

        {/* Message Input + Send Button */}
        <div className="input-row">
          <textarea
            className="message-input"
            placeholder="Ask me anything about ICT... (Press Enter to send)"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={isLoading || !inputText.trim()}
            title="Send message"
          >
            ➤
          </button>
        </div>
      </div>

      {/* ===================== LOGIN QUIZ MODAL ===================== */}
      {showQuiz && loginQuiz && (
        <LoginQuiz
          quiz={loginQuiz}
          studentId={STUDENT_ID}
          onClose={() => setShowQuiz(false)}
        />
      )}

      {/* ===================== TEACHER DASHBOARD ===================== */}
      {showTeacher && (
        <TeacherDashboard
          onClose={() => setShowTeacher(false)}
        />
      )}

    </div>
  );
}

export default App;
