"""
chatbot_engine.py
==================
This is the MAIN BRAIN of the chatbot.
It connects ALL modules together and decides what to do
for every student message.

Flow for every message:
------------------------
1. Receive student question + emotion state
2. Detect intent (exam or learning mode)
3. Find best answer from knowledge base
4. Adapt response based on emotion
5. Check for repeated questions (teacher alert)
6. Update difficulty level
7. Return final response

Works INDEPENDENTLY - does not need other team members' components.
When emotion data arrives from Tharaka's component, it uses it.
If not available, it detects emotion from text itself.
"""

import os
import pickle
import json
from datetime import datetime

from modules.knowledge_base import KnowledgeBase
from modules.emotion_adapter import adapt_response, detect_emotion_from_text, get_visual_suggestion
from modules.quiz_manager import QuizManager
from modules.teacher_alert import TeacherAlertSystem


class ChatbotEngine:
    """
    The main chatbot class that handles all student interactions.
    """

    def __init__(self):
        # Initialize all modules
        self.knowledge_base = KnowledgeBase()
        self.quiz_manager = QuizManager()
        self.teacher_alert = TeacherAlertSystem()
        self.intent_classifier = None

        # Track conversation history per student
        # Format: { student_id: [ {role, message, timestamp} ] }
        self.conversation_history = {}

        # Track student concept re-entry
        # Format: { student_id: { topic: last_asked_timestamp } }
        self.topic_history = {}

        self.is_ready = False

    def initialize(self):
        """
        Loads all AI models and knowledge base.
        Call this once when the server starts.
        """
        print("\n" + "="*50)
        print("Initializing ICT Chatbot Engine...")
        print("="*50)

        # Load knowledge base
        kb_loaded = self.knowledge_base.load()
        if not kb_loaded:
            print("WARNING: Knowledge base not loaded. Run training scripts first.")

        # Connect quiz manager to knowledge base
        self.quiz_manager.knowledge_base = self.knowledge_base

        # Load intent classifier
        intent_loaded = self._load_intent_classifier()
        if not intent_loaded:
            print("WARNING: Intent classifier not loaded. Using rule-based detection.")

        self.is_ready = True
        print("\nChatbot Engine is ready!")
        print("="*50 + "\n")
        return self.is_ready

    def _load_intent_classifier(self):
        """
        Loads the trained intent classifier model.
        Falls back to rule-based if model not found.
        """
        model_path = os.path.join("backend", "models", "intent_classifier.pkl")

        if not os.path.exists(model_path):
            print("  Intent classifier model not found. Using rule-based detection.")
            return False

        try:
            with open(model_path, 'rb') as f:
                self.intent_classifier = pickle.load(f)
            print("  Intent classifier loaded successfully.")
            return True
        except Exception as e:
            print(f"  Error loading intent classifier: {e}")
            return False

    # ===============================================================
    # MAIN CHAT FUNCTION
    # This is called for every student message
    # ===============================================================

    def chat(self, message, student_id="student_1", emotion_state=None):
        """
        Main function - processes a student message and returns a response.

        Parameters:
        -----------
        message      : The student's question/message text
        student_id   : Unique ID for the student
        emotion_state: Emotion from webcam detection (optional)
                       Can be: "confused", "bored", "distracted", 
                               "understanding", "neutral", or None

        Returns:
        --------
        dict with everything the frontend needs to display
        """

        # ---- Step 1: Basic validation ----
        if not message or not message.strip():
            return self._empty_message_response()

        message = message.strip()

        # ---- Step 2: Detect emotion ----
        # Use webcam emotion if available, otherwise detect from text
        if not emotion_state:
            emotion_state = detect_emotion_from_text(message)

        # ---- Step 3: Detect intent (exam or learning mode) ----
        intent = self._detect_intent(message)

        # ---- Step 4: Check for concept re-entry ----
        re_entry_message = self._check_concept_reentry(student_id, message)

        # ---- Step 5: Search knowledge base for answer ----
        search_result = self.knowledge_base.find_answer(message)

        # ---- Step 6: Adapt response based on emotion ----
        if search_result['found']:
            difficulty = self.quiz_manager.get_difficulty_level(
                student_id, search_result.get('topic', '')
            )
            adapted_answer = adapt_response(
                search_result['answer'],
                emotion_state,
                intent,
                difficulty=difficulty,
                student_id=student_id,
                question=message
            )
        else:
            adapted_answer = search_result['answer']

        # ---- Step 7: Get visual suggestion if confused ----
        visual = None
        if search_result['found']:
            visual = get_visual_suggestion(
                search_result.get('topic', ''),
                emotion_state
            )

        # ---- Step 8: Check for repeated questions (teacher alert) ----
        alert_result = self.teacher_alert.record_question(
            student_id,
            message,
            search_result.get('topic', 'Unknown')
        )

        # ---- Step 9: Check difficulty escalation ----
        difficulty_message = None
        if search_result['found']:
            topic = search_result.get('topic', '')
            difficulty_message = self.quiz_manager.get_difficulty_message(
                student_id, topic
            )

        # ---- Step 10: Save conversation history ----
        self._save_to_history(student_id, message, adapted_answer)

        # ---- Step 11: Build final response ----
        response = {
            "success": True,
            "message": adapted_answer,
            "intent": intent,
            "emotion_detected": emotion_state,
            "topic": search_result.get('topic'),
            "confidence": search_result.get('confidence', 0),
            "matched_question": search_result.get('matched_question'),
            "found_answer": search_result['found'],
            "visual_suggestion": visual,
            "teacher_alert": alert_result if alert_result.get('alert_triggered') else None,
            "difficulty_message": difficulty_message,
            "re_entry_message": re_entry_message,
            "timestamp": datetime.now().isoformat()
        }

        # Add student-facing alert if triggered
        if alert_result.get('alert_triggered'):
            response["alert_message"] = alert_result.get('alert_message')

        return response

    def request_micro_challenge(self, student_id, topic):
        """
        Called when student clicks "Try Challenge" button.
        Returns a micro challenge question.
        """
        challenge = self.quiz_manager.get_micro_challenge(topic, student_id)

        if not challenge:
            return {
                "success": False,
                "message": "No challenge available for this topic right now."
            }

        return {
            "success": True,
            "challenge": challenge
        }

    def submit_micro_challenge(self, student_id, student_answer, correct_answer, topic):
        """
        Called when student submits their micro challenge answer.
        """
        result = self.quiz_manager.check_micro_challenge_answer(
            student_answer, correct_answer, topic, student_id
        )

        return {
            "success": True,
            "result": result
        }

    def get_login_quiz(self, student_id):
        """
        Called when student logs in.
        Returns a set of quiz questions based on forgetting curve.
        """
        quiz = self.quiz_manager.get_login_quiz(student_id)

        if not quiz:
            return {
                "success": False,
                "message": "No quiz available right now. Start learning!",
                "has_quiz": False
            }

        return {
            "success": True,
            "has_quiz": True,
            "quiz": quiz
        }

    def submit_login_quiz(self, student_id, results):
        """
        Called when student submits login quiz answers.
        """
        feedback = self.quiz_manager.submit_login_quiz_results(student_id, results)

        return {
            "success": True,
            "feedback": feedback
        }

    def get_conversation_history(self, student_id, limit=10):
        """
        Returns the last N messages in the conversation.
        """
        history = self.conversation_history.get(student_id, [])
        return history[-limit:]

    def get_teacher_alerts(self, student_id=None):
        """
        Returns all teacher alerts.
        Called by the teacher dashboard.
        """
        alerts = self.teacher_alert.get_all_alerts(student_id)
        return {
            "success": True,
            "alerts": alerts,
            "total": len(alerts)
        }

    def get_student_progress(self, student_id):
        """
        Returns a summary of student progress.
        """
        progress = self.quiz_manager.get_student_summary(student_id)
        struggling = self.teacher_alert.get_struggling_topics(student_id)

        return {
            "success": True,
            "progress": progress,
            "struggling_topics": struggling,
            "total_questions": self.teacher_alert.get_student_question_count(student_id)
        }

    # ===============================================================
    # HELPER METHODS
    # ===============================================================

    def _detect_intent(self, message):
        """
        Detects whether the message is exam mode or learning mode.

        STRICT RULE:
        Only classify as EXAM if the message contains CLEAR exam keywords.
        Simple questions like "What is data?" are LEARNING by default.
        """
        message_lower = message.lower().strip()

        # These are STRONG exam signals - must be present to trigger exam mode
        strong_exam_keywords = [
            'define ',        # "define database"
            'state ',         # "state the function"
            ' marks',         # "2 marks", "4 marks"
            ' mark',          # "2 mark question"
            'for exam',       # "for exam"
            'exam question',  # "exam question"
            'exam answer',    # "exam answer"
            'briefly explain',
            'short note',
            'write short',
            'give definition',
            'full form of',
            'stand for',
            'name two ',
            'name three ',
            'name four ',
            'list two ',
            'list three ',
            'list four ',
            'mention two ',
            'mention three ',
            'state two ',
            'state three ',
        ]

        # Check strong exam keywords first
        for keyword in strong_exam_keywords:
            if keyword in message_lower:
                return "exam"

        # Message starts with "define" (without space after)
        if message_lower.startswith('define '):
            return "exam"

        # Has a number + marks pattern like "(2 marks)" or "2marks"
        import re
        if re.search(r'\d+\s*marks?', message_lower):
            return "exam"

        # Everything else is LEARNING mode
        # "What is X?", "How does X work?", "Explain X" etc
        return "learning"

    def _check_concept_reentry(self, student_id, message):
        """
        Detects if a student is returning to a topic they studied before.
        Returns a message to bridge old and new knowledge.
        """
        if student_id not in self.topic_history:
            self.topic_history[student_id] = {}
            return None

        # Check if any previously studied topic appears in this message
        message_lower = message.lower()

        for topic, last_asked in self.topic_history.get(student_id, {}).items():
            if topic.lower() in message_lower:
                time_diff = (datetime.now() - datetime.fromisoformat(last_asked)).days
                if time_diff >= 1:  # Returning after at least 1 day
                    self.topic_history[student_id][topic] = datetime.now().isoformat()
                    return f"🔄 Welcome back to '{topic}'! Let's do a quick refresh before we continue."

        return None

    def _save_to_history(self, student_id, message, response):
        """
        Saves the conversation to history.
        """
        if student_id not in self.conversation_history:
            self.conversation_history[student_id] = []

        self.conversation_history[student_id].append({
            "role": "student",
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

        self.conversation_history[student_id].append({
            "role": "chatbot",
            "message": response,
            "timestamp": datetime.now().isoformat()
        })

        # Keep only last 50 messages to save memory
        if len(self.conversation_history[student_id]) > 50:
            self.conversation_history[student_id] = \
                self.conversation_history[student_id][-50:]

    def _empty_message_response(self):
        return {
            "success": False,
            "message": "Please type a question so I can help you! 😊",
            "intent": None,
            "emotion_detected": None,
            "topic": None,
            "found_answer": False,
            "timestamp": datetime.now().isoformat()
        }
