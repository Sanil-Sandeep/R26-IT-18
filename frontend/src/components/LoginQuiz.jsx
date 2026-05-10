/**
 * LoginQuiz.jsx
 * ==============
 * This component shows a quiz popup when the student logs in.
 * Based on the forgetting curve - reviews topics studied days ago.
 * 
 * Flow:
 * 1. Quiz questions are shown one at a time
 * 2. Student types answers
 * 3. On submit, results are shown with feedback
 * 4. Student closes quiz and starts chatting
 */

import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function LoginQuiz({ quiz, studentId, onClose }) {
  // Store student's answers for each question
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // Update answer for a specific question
  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  // Submit all quiz answers
  const handleSubmit = async () => {
    setLoading(true);

    // Build results array to send to API
    const quizResults = quiz.questions.map((q) => ({
      question: q.question,
      student_answer: answers[q.question_id] || '',
      correct_answer: q.answer,
      topic: q.topic
    }));

    try {
      const response = await axios.post(`${API_URL}/quiz/login/submit`, {
        student_id: studentId,
        results: quizResults
      });

      if (response.data.success) {
        setResults(response.data.feedback);
        setSubmitted(true);
      }
    } catch (error) {
      console.error('Quiz submit error:', error);
    }

    setLoading(false);
  };

  // Get score emoji based on percentage
  const getScoreEmoji = (percentage) => {
    if (percentage >= 80) return '🌟';
    if (percentage >= 60) return '👍';
    if (percentage >= 40) return '📚';
    return '💪';
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">

        {/* Header */}
        <div className="modal-header">
          <div className="modal-emoji">🧠</div>
          <h2>Welcome Back!</h2>
          <p>
            {submitted
              ? 'Here are your results!'
              : `Quick revision quiz — ${quiz.total_questions} questions based on what you've studied`
            }
          </p>
        </div>

        {/* Quiz Questions */}
        {!submitted && (
          <>
            {quiz.questions.map((q) => (
              <div key={q.question_id} className="quiz-question">
                <div className="question-number">
                  Question {q.question_number} of {quiz.total_questions} • {q.topic}
                </div>
                <p>{q.question}</p>
                <input
                  className="quiz-input"
                  type="text"
                  placeholder="Type your answer..."
                  value={answers[q.question_id] || ''}
                  onChange={(e) => handleAnswerChange(q.question_id, e.target.value)}
                  onKeyDown={(e) => {
                    // Move to next input on Enter
                    if (e.key === 'Enter') e.target.blur();
                  }}
                />
              </div>
            ))}

            <button
              className="quiz-submit-btn"
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? 'Checking answers...' : '✓ Submit Answers'}
            </button>
          </>
        )}

        {/* Results */}
        {submitted && results && (
          <div className="quiz-result">
            <div className="result-emoji">
              {getScoreEmoji(results.percentage)}
            </div>
            <h3>{results.score}/{results.total} Correct</h3>
            <p style={{ fontSize: '24px', fontWeight: '700', color: '#667eea' }}>
              {results.percentage?.toFixed(0)}%
            </p>
            <p>{results.feedback}</p>

            {/* Topics that need revision */}
            {results.needs_revision && results.needs_revision.length > 0 && (
              <div className="revision-topics">
                📖 Topics to revise: {results.needs_revision.join(', ')}
              </div>
            )}

            <p style={{ fontSize: '13px', color: '#718096', marginTop: '8px' }}>
              {results.revision_message}
            </p>

            <button className="close-quiz-btn" onClick={onClose}>
              Start Learning 🚀
            </button>
          </div>
        )}

      </div>
    </div>
  );
}

export default LoginQuiz;
