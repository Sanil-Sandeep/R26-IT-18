"""
quiz_manager.py
================
This module handles ALL quiz-related features:

1. MICRO CHALLENGE  - Optional quick question before showing answer
2. LOGIN QUIZ       - Short quiz when student logs in (forgetting curve)
3. DIFFICULTY       - Tracks how well student is doing and adjusts difficulty
4. SCORE TRACKING   - Remembers quiz scores per topic

No database needed for basic operation - uses simple in-memory storage.
When MongoDB is connected, scores are saved permanently.
"""

import random
import json
from datetime import datetime, timedelta


class QuizManager:
    """
    Manages all quiz and challenge features of the chatbot.
    """

    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base

        # In-memory storage (works without MongoDB)
        # Format: { student_id: { topic: { score, last_seen, attempts } } }
        self.student_progress = {}

        # Difficulty levels
        self.DIFFICULTY_LEVELS = {
            1: "basic",      # Simple recall questions
            2: "medium",     # Understanding questions
            3: "advanced"    # Application questions
        }


    # MICRO CHALLENGE
    # A quick optional question before the chatbot shows the answer


    def get_micro_challenge(self, topic, student_id="default"):
        """
        Returns a micro-challenge question related to the current topic.
        This is shown BEFORE the chatbot answers, as an optional challenge.

        Returns:
        --------
        dict with:
        - question     : The challenge question
        - answer       : The correct answer (shown only if wrong)
        - topic        : What topic this is about
        - challenge_id : Unique ID for this challenge
        """

        if not self.knowledge_base or not self.knowledge_base.is_loaded:
            return None

        # Get a random question from this topic
        questions = self.knowledge_base.get_random_questions(count=1, topic=topic)

        if not questions:
            # If no topic-specific question, get any random question
            questions = self.knowledge_base.get_random_questions(count=1)

        if not questions:
            return None

        qa = questions[0]
        challenge_id = f"mc_{student_id}_{datetime.now().timestamp()}"

        return {
            "type": "micro_challenge",
            "challenge_id": challenge_id,
            "question": qa['question'],
            "answer": qa['answer'],
            "topic": qa.get('topic', 'General'),
            "message": "Want to try a quick challenge before the answer? 🎯"
        }

    def check_micro_challenge_answer(self, student_answer, correct_answer, topic, student_id="default"):
        """
        Checks if the student's answer to the micro challenge is correct.

        Uses simple keyword matching - if key words from the correct answer
        appear in the student's answer, it's considered correct.

        Returns:
        --------
        dict with:
        - correct      : True or False
        - feedback     : Message to show the student
        - show_summary : Whether to show lesson summary link
        """

        # Simple keyword matching
        correct_keywords = self._extract_keywords(correct_answer)
        student_keywords = self._extract_keywords(student_answer)

        # Count how many key words matched
        matches = len(correct_keywords.intersection(student_keywords))
        match_ratio = matches / len(correct_keywords) if correct_keywords else 0

        # Consider correct if 40%+ keywords match
        is_correct = match_ratio >= 0.4

        # Update student progress
        self._update_progress(student_id, topic, is_correct)

        if is_correct:
            return {
                "correct": True,
                "feedback": f"✅ Great job! That's correct! \n\nCorrect answer: {correct_answer}",
                "show_summary": False,
                "score_update": "+1"
            }
        else:
            return {
                "correct": False,
                "feedback": (
                    f"❌ Not quite right. Here's the correct answer:\n\n"
                    f"{correct_answer}\n\n"
                    f"It seems you might need a quick revision of this topic."
                ),
                "show_summary": True,
                "topic": topic,
                "summary_message": "📖 Would you like to see a summary of this topic?",
                "score_update": "0"
            }


    # LOGIN QUIZ (Forgetting Curve)
    # Shown when student logs in, based on topics they studied before


    def get_login_quiz(self, student_id="default", num_questions=5):
        """
        Generates a login quiz based on the forgetting curve.

        The forgetting curve says:
        - After 1 day  → 70% of info is forgotten
        - After 3 days → 80% forgotten
        - After 7 days → 90% forgotten

        So we quiz students on topics they studied a few days ago.

        Returns:
        --------
        A list of quiz questions, or None if no quiz needed
        """

        if not self.knowledge_base or not self.knowledge_base.is_loaded:
            return None

        # Get topics that need review based on time
        topics_to_review = self._get_topics_needing_review(student_id)

        if not topics_to_review:
            # No topics need review yet - get random questions
            questions = self.knowledge_base.get_random_questions(count=num_questions)
        else:
            # Get questions from topics that need review
            questions = []
            for topic in topics_to_review[:3]:  # Review up to 3 topics
                topic_questions = self.knowledge_base.get_random_questions(
                    count=2,
                    topic=topic
                )
                questions.extend(topic_questions)

            # Fill remaining slots with random questions
            remaining = num_questions - len(questions)
            if remaining > 0:
                extra = self.knowledge_base.get_random_questions(count=remaining)
                questions.extend(extra)

        if not questions:
            return None

        # Format questions for the quiz
        quiz_questions = []
        for i, qa in enumerate(questions[:num_questions]):
            quiz_questions.append({
                "question_number": i + 1,
                "question": qa['question'],
                "answer": qa['answer'],
                "topic": qa.get('topic', 'General'),
                "question_id": f"lq_{i}_{student_id}"
            })

        return {
            "type": "login_quiz",
            "total_questions": len(quiz_questions),
            "questions": quiz_questions,
            "message": f"👋 Welcome back! Quick check on what you've learned - {len(quiz_questions)} questions:"
        }

    def submit_login_quiz_results(self, student_id, results):
        """
        Processes login quiz results and gives feedback.

        Parameters:
        -----------
        student_id : The student's ID
        results    : List of { question, student_answer, correct_answer, topic }

        Returns:
        --------
        dict with score, feedback, and topics that need revision
        """

        correct_count = 0
        needs_revision = []

        for result in results:
            topic = result.get('topic', 'General')
            student_answer = result.get('student_answer', '')
            correct_answer = result.get('correct_answer', '')

            # Check answer
            check = self.check_micro_challenge_answer(
                student_answer, correct_answer, topic, student_id
            )

            if check['correct']:
                correct_count += 1
            else:
                if topic not in needs_revision:
                    needs_revision.append(topic)

        total = len(results)
        score_percent = (correct_count / total * 100) if total > 0 else 0

        # Update forgetting curve data
        if score_percent >= 80:
            reduction_factor = 2  # Reduce quiz frequency for well-known topics
        else:
            reduction_factor = 1  # Keep quizzing on weak topics

        # Build response
        if score_percent >= 80:
            feedback = (
                f"🌟 Excellent! You got {correct_count}/{total} correct ({score_percent:.0f}%)!\n"
                f"You remember these topics well. Keep it up!"
            )
        elif score_percent >= 50:
            feedback = (
                f"👍 Good effort! You got {correct_count}/{total} correct ({score_percent:.0f}%).\n"
                f"A little more revision will help!"
            )
        else:
            feedback = (
                f"📚 You got {correct_count}/{total} correct ({score_percent:.0f}%).\n"
                f"It looks like you need to revise some topics."
            )

        return {
            "score": correct_count,
            "total": total,
            "percentage": score_percent,
            "feedback": feedback,
            "needs_revision": needs_revision,
            "revision_message": (
                f"📖 Topics to revise: {', '.join(needs_revision)}"
                if needs_revision else "✅ No revision needed right now!"
            )
        }

  
    # DIFFICULTY ESCALATION
    # Increases challenge level as student answers correctly
   

    def get_difficulty_level(self, student_id="default", topic=None):
        """
        Returns the current difficulty level for a student.
        Starts at 1 (basic) and increases as student does well.
        """
        if student_id not in self.student_progress:
            return 1

        if topic:
            topic_data = self.student_progress[student_id].get(topic, {})
            score = topic_data.get('consecutive_correct', 0)
        else:
            # Get overall score
            all_scores = [
                v.get('consecutive_correct', 0)
                for v in self.student_progress.get(student_id, {}).values()
            ]
            score = sum(all_scores) / len(all_scores) if all_scores else 0

        # Escalate difficulty based on consecutive correct answers
        if score >= 5:
            return 3  # Advanced
        elif score >= 3:
            return 2  # Medium
        else:
            return 1  # Basic

    def get_difficulty_message(self, student_id, topic):
        """
        Returns a message about difficulty escalation when student is doing well.
        """
        level = self.get_difficulty_level(student_id, topic)

        if level == 2:
            return "🎯 You're doing well! Let's try something a bit harder."
        elif level == 3:
            return "🔥 Excellent! You've reached advanced level for this topic!"
        return None

   
    # HELPER METHODS
    

    def _extract_keywords(self, text):
        """
        Extracts important keywords from text for answer checking.
        Removes common words like 'the', 'a', 'is', etc.
        """
        if not text:
            return set()

        # Common words to ignore
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'shall', 'can',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'that', 'this', 'these', 'those', 'it', 'its', 'which',
            'and', 'or', 'but', 'not', 'so', 'if', 'as', 'into', 'about'
        }

        words = text.lower().split()
        keywords = set()

        for word in words:
            # Remove punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            if clean_word and clean_word not in stop_words and len(clean_word) > 2:
                keywords.add(clean_word)

        return keywords

    def _update_progress(self, student_id, topic, is_correct):
        """
        Updates the student's progress data after answering a question.
        """
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {}

        if topic not in self.student_progress[student_id]:
            self.student_progress[student_id][topic] = {
                'correct': 0,
                'total': 0,
                'consecutive_correct': 0,
                'last_studied': datetime.now().isoformat(),
                'last_score': 0
            }

        progress = self.student_progress[student_id][topic]
        progress['total'] += 1
        progress['last_studied'] = datetime.now().isoformat()

        if is_correct:
            progress['correct'] += 1
            progress['consecutive_correct'] += 1
        else:
            progress['consecutive_correct'] = 0

        progress['last_score'] = (progress['correct'] / progress['total']) * 100

    def _get_topics_needing_review(self, student_id):
        """
        Based on forgetting curve logic, returns topics that need review.

        Forgetting curve:
        - Studied 1-2 days ago → needs review
        - Studied 3-7 days ago → definitely needs review
        - Studied today → no review needed
        """
        if student_id not in self.student_progress:
            return []

        needs_review = []
        now = datetime.now()

        for topic, data in self.student_progress[student_id].items():
            last_studied_str = data.get('last_studied', '')
            if not last_studied_str:
                continue

            try:
                last_studied = datetime.fromisoformat(last_studied_str)
                days_ago = (now - last_studied).days

                # Review if studied 1+ days ago
                if days_ago >= 1:
                    needs_review.append(topic)
            except:
                continue

        return needs_review

    def get_student_summary(self, student_id):
        """
        Returns a summary of the student's overall progress.
        """
        if student_id not in self.student_progress:
            return {"message": "No progress recorded yet. Start asking questions!"}

        progress = self.student_progress[student_id]
        total_correct = sum(v['correct'] for v in progress.values())
        total_attempts = sum(v['total'] for v in progress.values())
        overall_score = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

        weak_topics = [
            topic for topic, data in progress.items()
            if data.get('last_score', 100) < 50
        ]

        return {
            "total_questions_attempted": total_attempts,
            "total_correct": total_correct,
            "overall_score": f"{overall_score:.1f}%",
            "topics_studied": list(progress.keys()),
            "weak_topics": weak_topics,
            "message": f"Overall score: {overall_score:.1f}% across {len(progress)} topics"
        }