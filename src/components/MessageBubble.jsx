/**
 * MessageBubble.jsx
 * ==================
 * Displays a single chat message bubble.
 * 
 * Shows different styles for:
 * - Student messages (right side, purple)
 * - Chatbot messages (left side, white)
 * 
 * Also shows:
 * - Intent badge (📝 EXAM or 📚 LEARN)
 * - Confidence bar
 * - Visual suggestion
 * - Teacher alert message
 * - Re-entry message
 * - Micro challenge buttons
 */

import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function MessageBubble({ message, studentId }) {
  // State for micro challenge
  const [showChallenge, setShowChallenge] = useState(false);
  const [challengeData, setChallengeData] = useState(null);
  const [challengeAnswer, setChallengeAnswer] = useState('');
  const [challengeResult, setChallengeResult] = useState(null);
  const [loadingChallenge, setLoadingChallenge] = useState(false);

  const isBot = message.role === 'chatbot';
  const isStudent = message.role === 'student';

  // ---- Request Micro Challenge ----
  const handleTryChallenge = async () => {
    setLoadingChallenge(true);
    try {
      const response = await axios.post(`${API_URL}/chat/challenge`, {
        student_id: studentId,
        topic: message.topic || null
      });

      if (response.data.success) {
        setChallengeData(response.data.challenge);
        setShowChallenge(true);
      }
    } catch (error) {
      console.error('Challenge error:', error);
    }
    setLoadingChallenge(false);
  };

  // ---- Submit Challenge Answer ----
  const handleSubmitChallenge = async () => {
    if (!challengeAnswer.trim() || !challengeData) return;

    try {
      const response = await axios.post(`${API_URL}/chat/challenge/submit`, {
        student_id: studentId,
        student_answer: challengeAnswer,
        correct_answer: challengeData.answer,
        topic: challengeData.topic
      });

      if (response.data.success) {
        setChallengeResult(response.data.result);
      }
    } catch (error) {
      console.error('Submit challenge error:', error);
    }
  };

  // ---- Skip Challenge ----
  const handleSkipChallenge = () => {
    setShowChallenge(false);
    setChallengeData(null);
    setChallengeResult(null);
    setChallengeAnswer('');
  };

  // ---- Render Student Message ----
  if (isStudent) {
    return (
      <div className="message-wrapper student">
        <div className="message-avatar student">🧑‍🎓</div>
        <div className="message-content">
          <div className="message-bubble student">
            {message.text}
          </div>
          <div className="message-meta" style={{ justifyContent: 'flex-end' }}>
            {formatTime(message.timestamp)}
          </div>
        </div>
      </div>
    );
  }

  // ---- Render Bot Message ----
  if (isBot) {
    return (
      <div className="message-wrapper chatbot">
        <div className="message-avatar bot">🤖</div>
        <div className="message-content" style={{ maxWidth: '100%' }}>

          {/* Main Answer Bubble */}
          <div className="message-bubble bot">
            {message.text}
          </div>

          {/* Confidence Bar */}
          {message.confidence > 0 && (
            <div className="confidence-bar" title={`Match confidence: ${(message.confidence * 100).toFixed(0)}%`}>
              <div
                className="confidence-fill"
                style={{ width: `${message.confidence * 100}%` }}
              />
            </div>
          )}

          {/* Meta info: time, intent, topic */}
          <div className="message-meta">
            <span>{formatTime(message.timestamp)}</span>
            {message.intent && (
              <span className={`intent-badge intent-${message.intent}`}>
                {message.intent === 'exam' ? '📝 Exam' : '📚 Learning'}
              </span>
            )}
            {message.topic && (
              <span>📌 {message.topic}</span>
            )}
          </div>

          {/* Visual Suggestion */}
          {message.visual_suggestion && (
            <div className="visual-suggestion">
              {message.visual_suggestion}
            </div>
          )}

          {/* Re-entry message (returning to old topic) */}
          {message.re_entry_message && (
            <div className="reentry-message">
              {message.re_entry_message}
            </div>
          )}

          {/* Teacher Alert */}
          {message.alert_message && (
            <div className="alert-message">
              ⚠️ {message.alert_message}
            </div>
          )}

          {/* Micro Challenge Buttons */}
          {message.found_answer && !showChallenge && !challengeResult && (
            <div className="challenge-buttons">
              <button
                className="btn-challenge btn-try"
                onClick={handleTryChallenge}
                disabled={loadingChallenge}
              >
                {loadingChallenge ? '...' : '🎯 Try Challenge'}
              </button>
            </div>
          )}

          {/* Challenge Question */}
          {showChallenge && challengeData && !challengeResult && (
            <div className="challenge-box">
              <h4>🎯 Quick Challenge</h4>
              <p>{challengeData.question}</p>
              <input
                className="challenge-input"
                type="text"
                placeholder="Type your answer here..."
                value={challengeAnswer}
                onChange={(e) => setChallengeAnswer(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmitChallenge()}
              />
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="btn-submit" onClick={handleSubmitChallenge}>
                  Submit ✓
                </button>
                <button
                  className="btn-challenge btn-skip"
                  onClick={handleSkipChallenge}
                >
                  Skip
                </button>
              </div>
            </div>
          )}

          {/* Challenge Result */}
          {challengeResult && (
            <div className={`challenge-result ${challengeResult.correct ? 'correct' : 'wrong'}`}>
              {challengeResult.feedback}
              {challengeResult.show_summary && (
                <div style={{ marginTop: '8px', fontWeight: '500' }}>
                  {challengeResult.summary_message}
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    );
  }

  return null;
}

// Helper: format timestamp to readable time
function formatTime(timestamp) {
  if (!timestamp) return '';
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } catch {
    return '';
  }
}

export default MessageBubble;
