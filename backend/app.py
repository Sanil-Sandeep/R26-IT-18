"""
app.py
=======
This is the main Flask server (API) for the ICT Chatbot.

It creates a web server that listens for requests from the frontend
and sends back responses from the chatbot engine.

API Endpoints (URLs the frontend can call):
--------------------------------------------
POST /api/chat              → Send a message, get a response
POST /api/chat/challenge    → Request a micro challenge
POST /api/chat/challenge/submit → Submit micro challenge answer
GET  /api/quiz/login        → Get login quiz questions
POST /api/quiz/login/submit → Submit login quiz answers
GET  /api/student/progress  → Get student progress summary
GET  /api/teacher/alerts    → Get all teacher alerts (teacher view)
GET  /api/health            → Check if server is running
GET  /api/topics            → Get all available topics

How to run:
-----------
python backend/app.py
"""

import os
import sys

# Add backend folder to path so Python can find the modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Import our chatbot engine
from modules.chatbot_engine import ChatbotEngine


# CREATE FLASK APP

app = Flask(__name__)

# CORS allows the React frontend (running on different port) to talk to this server
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


# CREATE CHATBOT ENGINE (one instance for entire app)

chatbot = ChatbotEngine()



# STARTUP
# Load all models when server starts

@app.before_request
def startup():
    """Initialize chatbot on first request."""
    global chatbot
    if not chatbot.is_ready:
        chatbot.initialize()



# API ENDPOINT 1: HEALTH CHECK
# URL: GET /api/health
# Used to check if the server is running properly

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Simple check to see if the server is running.
    Frontend calls this when it loads to confirm connection.
    """
    return jsonify({
        "status": "running",
        "chatbot_ready": chatbot.is_ready,
        "knowledge_base_loaded": chatbot.knowledge_base.is_loaded,
        "timestamp": datetime.now().isoformat(),
        "message": "ICT Chatbot API is running!"
    })



# API ENDPOINT 2: MAIN CHAT
# URL: POST /api/chat
# This is the most important endpoint - handles all student messages

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Receives a student message and returns the chatbot response.

    Request body (JSON):
    --------------------
    {
        "message"      : "What is a database?",      ← required
        "student_id"   : "student_123",               ← optional (default: "student_1")
        "emotion_state": "confused"                   ← optional (from webcam detection)
    }

    Response (JSON):
    ----------------
    {
        "success"          : true,
        "message"          : "A database is...",
        "intent"           : "learning",
        "emotion_detected" : "confused",
        "topic"            : "Chapter 1",
        "confidence"       : 0.95,
        "visual_suggestion": "📊 Visual: Database table diagram",
        "teacher_alert"    : null,
        "timestamp"        : "2026-01-01T10:00:00"
    }
    """

    # Get the data sent from frontend
    data = request.get_json()

    # Validate - make sure message exists
    if not data:
        return jsonify({
            "success": False,
            "message": "No data received. Please send a message.",
            "error": "missing_data"
        }), 400

    message = data.get('message', '').strip()

    if not message:
        return jsonify({
            "success": False,
            "message": "Please type a question!",
            "error": "empty_message"
        }), 400

    # Get optional parameters
    student_id = data.get('student_id', 'student_1')
    emotion_state = data.get('emotion_state', None)

    # Validate emotion state
    valid_emotions = ['confused', 'bored', 'distracted', 'understanding', 'neutral']
    if emotion_state and emotion_state not in valid_emotions:
        emotion_state = None  # Ignore invalid emotion

    try:
        # Send to chatbot engine
        response = chatbot.chat(
            message=message,
            student_id=student_id,
            emotion_state=emotion_state
        )
        return jsonify(response)

    except Exception as e:
        print(f"Error in /api/chat: {e}")
        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again.",
            "error": str(e)
        }), 500



# API ENDPOINT 3: REQUEST MICRO CHALLENGE
# URL: POST /api/chat/challenge
# Called when student clicks "Try Challenge" button

@app.route('/api/chat/challenge', methods=['POST'])
def request_challenge():
    """
    Returns a micro challenge question for the current topic.

    Request body (JSON):
    --------------------
    {
        "student_id": "student_123",
        "topic"     : "Chapter 1"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400

    student_id = data.get('student_id', 'student_1')
    topic = data.get('topic', None)

    try:
        result = chatbot.request_micro_challenge(student_id, topic)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 4: SUBMIT MICRO CHALLENGE ANSWER
# URL: POST /api/chat/challenge/submit
# Called when student submits their challenge answer

@app.route('/api/chat/challenge/submit', methods=['POST'])
def submit_challenge():
    """
    Checks the student's micro challenge answer.

    Request body (JSON):
    --------------------
    {
        "student_id"    : "student_123",
        "student_answer": "A database stores data electronically",
        "correct_answer": "A database is an organized collection...",
        "topic"         : "Chapter 1"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400

    student_id = data.get('student_id', 'student_1')
    student_answer = data.get('student_answer', '')
    correct_answer = data.get('correct_answer', '')
    topic = data.get('topic', 'Unknown')

    try:
        result = chatbot.submit_micro_challenge(
            student_id, student_answer, correct_answer, topic
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 5: GET LOGIN QUIZ
# URL: GET /api/quiz/login?student_id=student_123
# Called when student logs in to get their quiz

@app.route('/api/quiz/login', methods=['GET'])
def get_login_quiz():
    """
    Returns a set of quiz questions when student logs in.
    Based on forgetting curve - focuses on topics studied days ago.
    """
    student_id = request.args.get('student_id', 'student_1')

    try:
        result = chatbot.get_login_quiz(student_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 6: SUBMIT LOGIN QUIZ
# URL: POST /api/quiz/login/submit
# Called when student finishes the login quiz

@app.route('/api/quiz/login/submit', methods=['POST'])
def submit_login_quiz():
    """
    Processes login quiz answers and returns feedback.

    Request body (JSON):
    --------------------
    {
        "student_id": "student_123",
        "results": [
            {
                "question"      : "What is a database?",
                "student_answer": "A place to store data",
                "correct_answer": "A database is...",
                "topic"         : "Chapter 1"
            },
            ...
        ]
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "message": "No data received"}), 400

    student_id = data.get('student_id', 'student_1')
    results = data.get('results', [])

    if not results:
        return jsonify({"success": False, "message": "No quiz results provided"}), 400

    try:
        result = chatbot.submit_login_quiz(student_id, results)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 7: STUDENT PROGRESS
# URL: GET /api/student/progress?student_id=student_123
# Returns student's learning progress summary

@app.route('/api/student/progress', methods=['GET'])
def student_progress():
    """
    Returns overall learning progress for a student.
    Shows scores, weak topics, and study history.
    """
    student_id = request.args.get('student_id', 'student_1')

    try:
        result = chatbot.get_student_progress(student_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 8: TEACHER ALERTS
# URL: GET /api/teacher/alerts
# Returns all alerts for the teacher dashboard

@app.route('/api/teacher/alerts', methods=['GET'])
def teacher_alerts():
    """
    Returns all student alerts for the teacher to see.
    Shows which students are struggling with which topics.
    """
    student_id = request.args.get('student_id', None)

    try:
        result = chatbot.get_teacher_alerts(student_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 9: GET ALL TOPICS
# URL: GET /api/topics
# Returns all available topics from the knowledge base

@app.route('/api/topics', methods=['GET'])
def get_topics():
    """
    Returns all topics available in the knowledge base.
    Used by frontend to show topic selector.
    """
    try:
        topics = chatbot.knowledge_base.get_all_topics()
        return jsonify({
            "success": True,
            "topics": topics,
            "total": len(topics)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# API ENDPOINT 10: CONVERSATION HISTORY
# URL: GET /api/chat/history?student_id=student_123
# Returns past messages for a student

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    """
    Returns the last 10 messages from the student's conversation.
    """
    student_id = request.args.get('student_id', 'student_1')
    limit = int(request.args.get('limit', 10))

    try:
        history = chatbot.get_conversation_history(student_id, limit)
        return jsonify({
            "success": True,
            "history": history,
            "student_id": student_id
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# ERROR HANDLERS
# These run when something goes wrong

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "message": "The URL you requested does not exist."
    }), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "Something went wrong on the server."
    }), 500



# RUN THE SERVER

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  ICT Chatbot API Server")
    print("="*50)
    print("  Starting server...")
    print("  URL: http://localhost:5000")
    print("  Press CTRL+C to stop")
    print("="*50 + "\n")

    # Initialize chatbot before starting
    chatbot.initialize()

    # Start Flask server
    # debug=True  → shows errors clearly (good for development)
    # host='0.0.0.0' → accessible from any device on same network
    # port=5000  → the port number (like a door number)
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=False  # Prevents loading models twice
    )