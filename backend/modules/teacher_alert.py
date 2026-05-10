"""
teacher_alert.py
=================
This module detects when a student is struggling with a topic
by tracking how many times they ask similar questions.

If the same question is asked 3+ times → Alert is sent to teacher.

This works completely independently - no other component needed.
"""

from datetime import datetime
from collections import defaultdict


class TeacherAlertSystem:
    """
    Monitors student questions and generates alerts when
    a student appears to be struggling with a concept.
    """

    def __init__(self):
        # Stores question history per student
        # Format: { student_id: [ {question, topic, timestamp} ] }
        self.question_history = defaultdict(list)

        # Stores generated alerts
        # Format: { student_id: [ {topic, count, timestamp, alert_message} ] }
        self.alerts = defaultdict(list)

        # How many times a question must be repeated to trigger alert
        self.REPEAT_THRESHOLD = 3

        # Similarity threshold for considering questions "the same"
        self.SIMILARITY_THRESHOLD = 0.6

    def record_question(self, student_id, question, topic):
        """
        Records every question a student asks.
        Then checks if they're struggling (asking same thing repeatedly).

        Parameters:
        -----------
        student_id : The student's ID
        question   : What the student asked
        topic      : What topic this question is about

        Returns:
        --------
        dict with:
        - alert_triggered : True if teacher should be notified
        - alert_message   : The message to send to teacher
        - repeat_count    : How many times this topic was asked
        """

        # Record this question
        self.question_history[student_id].append({
            "question": question,
            "topic": topic,
            "timestamp": datetime.now().isoformat()
        })

        # Check if student is struggling with this topic
        repeat_count = self._count_topic_repeats(student_id, topic)

        # Trigger alert if threshold reached
        if repeat_count >= self.REPEAT_THRESHOLD:
            alert = self._create_alert(student_id, topic, question, repeat_count)

            # Only add alert if not already alerted recently for same topic
            if not self._already_alerted(student_id, topic):
                self.alerts[student_id].append(alert)
                return {
                    "alert_triggered": True,
                    "alert_message": alert['alert_message'],
                    "teacher_message": alert['teacher_message'],
                    "repeat_count": repeat_count,
                    "topic": topic
                }

        return {
            "alert_triggered": False,
            "repeat_count": repeat_count,
            "topic": topic
        }

    def _count_topic_repeats(self, student_id, topic):
        """
        Counts how many times a student asked about the same topic.
        """
        history = self.question_history[student_id]
        topic_lower = topic.lower() if topic else ""

        count = sum(
            1 for entry in history
            if topic_lower in entry.get('topic', '').lower()
        )
        return count

    def _create_alert(self, student_id, topic, latest_question, count):
        """
        Creates an alert message for the teacher.
        """
        teacher_message = (
            f"⚠️ STUDENT ALERT\n"
            f"Student ID   : {student_id}\n"
            f"Topic        : {topic}\n"
            f"Repeat Count : {count} times\n"
            f"Latest Q     : '{latest_question}'\n"
            f"Time         : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Action       : Student appears to be struggling with '{topic}'. "
            f"Please provide additional support."
        )

        student_message = (
            f"I notice you've asked about '{topic}' several times. "
            f"It seems this topic might be challenging. "
            f"Your teacher has been notified and will help you soon! 👨‍🏫"
        )

        return {
            "student_id": student_id,
            "topic": topic,
            "repeat_count": count,
            "timestamp": datetime.now().isoformat(),
            "alert_message": student_message,
            "teacher_message": teacher_message
        }

    def _already_alerted(self, student_id, topic):
        """
        Checks if we already sent an alert for this topic recently.
        Prevents sending duplicate alerts.
        """
        recent_alerts = self.alerts[student_id]
        topic_lower = topic.lower() if topic else ""

        for alert in recent_alerts[-5:]:  # Check last 5 alerts
            if topic_lower in alert.get('topic', '').lower():
                return True
        return False

    def get_all_alerts(self, student_id=None):
        """
        Returns all alerts.
        If student_id is given, returns only that student's alerts.
        Used by the teacher dashboard.
        """
        if student_id:
            return self.alerts.get(student_id, [])

        # Return all alerts from all students
        all_alerts = []
        for sid, alert_list in self.alerts.items():
            for alert in alert_list:
                alert['student_id'] = sid
                all_alerts.append(alert)

        # Sort by most recent first
        all_alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return all_alerts

    def get_struggling_topics(self, student_id):
        """
        Returns a list of topics the student is struggling with.
        """
        history = self.question_history[student_id]
        topic_counts = defaultdict(int)

        for entry in history:
            topic = entry.get('topic', 'Unknown')
            topic_counts[topic] += 1

        # Return topics asked 2+ times
        struggling = {
            topic: count
            for topic, count in topic_counts.items()
            if count >= 2
        }

        return struggling

    def get_student_question_count(self, student_id):
        """
        Returns total number of questions a student has asked.
        """
        return len(self.question_history[student_id])