/**
 * TeacherDashboard.jsx
 * =====================
 * Shows a popup dashboard for the teacher to see:
 * - Which students are struggling
 * - Which topics are repeated
 * - Alert messages
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function TeacherDashboard({ onClose }) {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Load alerts when dashboard opens
  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/teacher/alerts`);
      if (response.data.success) {
        setAlerts(response.data.alerts);
      }
    } catch (error) {
      console.error('Error loading alerts:', error);
    }
    setLoading(false);
  };

  // Format date nicely
  const formatDate = (timestamp) => {
    if (!timestamp) return '';
    try {
      const date = new Date(timestamp);
      return date.toLocaleString();
    } catch {
      return timestamp;
    }
  };

  return (
    <div className="teacher-dashboard">
      <div className="dashboard-box">

        {/* Header */}
        <div className="dashboard-header">
          <h2>👨‍🏫 Teacher Dashboard</h2>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        {/* Content */}
        <div className="dashboard-content">

          <p style={{ fontSize: '13px', color: '#718096', marginBottom: '16px' }}>
            Students who have asked about the same topic 3+ times are shown below.
          </p>

          {/* Loading */}
          {loading && (
            <p style={{ textAlign: 'center', color: '#718096' }}>Loading alerts...</p>
          )}

          {/* No Alerts */}
          {!loading && alerts.length === 0 && (
            <div className="no-alerts">
              <div style={{ fontSize: '48px', marginBottom: '12px' }}>✅</div>
              <p>No alerts right now.</p>
              <p style={{ fontSize: '12px' }}>All students seem to be doing well!</p>
            </div>
          )}

          {/* Alert Cards */}
          {!loading && alerts.map((alert, index) => (
            <div key={index} className="alert-card">
              <div className="alert-header">
                <span className="alert-topic">⚠️ {alert.topic}</span>
                <span className="alert-count">
                  Asked {alert.repeat_count} times
                </span>
              </div>
              <div className="alert-body">
                {alert.teacher_message}
              </div>
              <div style={{ fontSize: '11px', color: '#a0aec0', marginTop: '8px' }}>
                {formatDate(alert.timestamp)}
              </div>
            </div>
          ))}

          {/* Refresh Button */}
          <button
            onClick={loadAlerts}
            style={{
              width: '100%',
              padding: '10px',
              background: '#f7fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '13px',
              fontFamily: 'Poppins, sans-serif',
              marginTop: '12px',
              color: '#4a5568'
            }}
          >
            🔄 Refresh Alerts
          </button>

        </div>
      </div>
    </div>
  );
}

export default TeacherDashboard;
