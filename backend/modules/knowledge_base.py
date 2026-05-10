"""
knowledge_base.py
=================
This module loads the FAISS knowledge base we built in Step 2
and uses it to find the best answer for any student question.

Think of this as the LIBRARIAN of the chatbot.
Student asks a question → Librarian searches → Returns best answer.
"""

import os
import json
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer



# SETTINGS

MODELS_FOLDER = os.path.join("backend", "models")
INDEX_FILE = os.path.join(MODELS_FOLDER, "faiss_index.pkl")
METADATA_FILE = os.path.join(MODELS_FOLDER, "qa_metadata.json")
MODEL_NAME = "all-MiniLM-L6-v2"

# Minimum confidence score to return an answer
# If similarity is below this, the chatbot says it doesn't know
MIN_CONFIDENCE = 0.3


class KnowledgeBase:
    """
    The KnowledgeBase class handles everything related to
    finding answers from the Q&A dataset.
    """

    def __init__(self):
        self.index = None        # FAISS search index
        self.qa_pairs = []       # All Q&A pairs
        self.model = None        # Sentence transformer model
        self.is_loaded = False   # Track if everything loaded correctly

    def load(self):
        """
        Loads the FAISS index, Q&A data, and AI model.
        Call this once when the chatbot starts up.
        """
        print("Loading Knowledge Base...")

        # Check if model files exist
        if not os.path.exists(INDEX_FILE):
            print(f"ERROR: FAISS index not found at {INDEX_FILE}")
            print("Please run build_knowledge_base.py first!")
            return False

        if not os.path.exists(METADATA_FILE):
            print(f"ERROR: Q&A metadata not found at {METADATA_FILE}")
            print("Please run build_knowledge_base.py first!")
            return False

        try:
            # Load the FAISS index
            print("  Loading FAISS search index...")
            with open(INDEX_FILE, 'rb') as f:
                self.index = pickle.load(f)

            # Load the Q&A metadata
            print("  Loading Q&A data...")
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            self.qa_pairs = metadata['qa_pairs']

            # Load the sentence transformer model
            print("  Loading sentence AI model...")
            self.model = SentenceTransformer(MODEL_NAME)

            self.is_loaded = True
            print(f"  Knowledge base ready! ({len(self.qa_pairs)} Q&A pairs loaded)")
            return True

        except Exception as e:
            print(f"ERROR loading knowledge base: {e}")
            return False

    def find_answer(self, question, top_k=3):
        """
        Finds the best answer for a given question.

        Parameters:
        -----------
        question : The student's question text
        top_k    : How many similar questions to look at (default 3)

        Returns:
        --------
        A dictionary with:
        - answer      : The best answer found
        - confidence  : How confident we are (0.0 to 1.0)
        - topic       : What chapter/topic this is from
        - matched_q   : The question we matched with
        - alternatives: Other possible answers (for low confidence)
        """

        if not self.is_loaded:
            return self._not_loaded_response()

        if not question or not question.strip():
            return self._empty_question_response()

        try:
            # Convert the student's question to a vector
            query_vector = self.model.encode(
                [question],
                normalize_embeddings=True,
                convert_to_numpy=True
            )

            # Search FAISS for the most similar questions
            distances, indices = self.index.search(
                query_vector.astype(np.float32),
                k=min(top_k, len(self.qa_pairs))
            )

            # Get the best match
            best_idx = indices[0][0]
            best_confidence = float(distances[0][0])

            # If confidence is too low, say we don't know
            if best_confidence < MIN_CONFIDENCE:
                return self._low_confidence_response(question)

            # Get the best matching Q&A pair
            best_qa = self.qa_pairs[best_idx]

            # Get alternative answers (2nd and 3rd best matches)
            alternatives = []
            for i in range(1, len(indices[0])):
                alt_idx = indices[0][i]
                alt_confidence = float(distances[0][i])
                if alt_confidence > MIN_CONFIDENCE and alt_idx < len(self.qa_pairs):
                    alternatives.append({
                        "question": self.qa_pairs[alt_idx]['question'],
                        "answer": self.qa_pairs[alt_idx]['answer'],
                        "confidence": alt_confidence
                    })

            return {
                "found": True,
                "answer": best_qa['answer'],
                "confidence": best_confidence,
                "topic": best_qa.get('topic', 'Unknown'),
                "source": best_qa.get('source', 'Unknown'),
                "matched_question": best_qa['question'],
                "alternatives": alternatives
            }

        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return self._error_response()

    def get_questions_by_topic(self, topic):
        """
        Returns all questions for a specific topic/chapter.
        Used by the quiz manager to get questions for the login quiz.
        """
        if not self.is_loaded:
            return []

        topic_lower = topic.lower()
        matching = [
            qa for qa in self.qa_pairs
            if topic_lower in qa.get('topic', '').lower() or
               topic_lower in qa.get('source', '').lower()
        ]
        return matching

    def get_random_questions(self, count=5, topic=None):
        """
        Returns random questions from the knowledge base.
        Used for micro-challenges and quizzes.
        """
        import random

        if not self.is_loaded:
            return []

        # Filter by topic if specified
        if topic:
            pool = self.get_questions_by_topic(topic)
        else:
            pool = self.qa_pairs

        # Return random selection
        count = min(count, len(pool))
        return random.sample(pool, count)

    def get_all_topics(self):
        """
        Returns a list of all available topics/chapters.
        """
        if not self.is_loaded:
            return []

        topics = list(set([qa.get('topic', '') for qa in self.qa_pairs]))
        return sorted([t for t in topics if t])

    # -------------------------------------------------------
    # HELPER RESPONSES
    # -------------------------------------------------------

    def _not_loaded_response(self):
        return {
            "found": False,
            "answer": "The knowledge base is not loaded yet. Please wait a moment and try again.",
            "confidence": 0.0,
            "topic": None,
            "matched_question": None,
            "alternatives": []
        }

    def _empty_question_response(self):
        return {
            "found": False,
            "answer": "Please type a question so I can help you!",
            "confidence": 0.0,
            "topic": None,
            "matched_question": None,
            "alternatives": []
        }

    def _low_confidence_response(self, question):
        return {
            "found": False,
            "answer": (
                f"I'm sorry, I don't have a specific answer for '{question}' in my knowledge base yet. "
                f"This might be from a topic I haven't learned yet. "
                f"Try rephrasing your question or ask your teacher for help."
            ),
            "confidence": 0.0,
            "topic": None,
            "matched_question": None,
            "alternatives": []
        }

    def _error_response(self):
        return {
            "found": False,
            "answer": "Something went wrong while searching. Please try again.",
            "confidence": 0.0,
            "topic": None,
            "matched_question": None,
            "alternatives": []
        }