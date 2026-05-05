"""
emotion_adapter.py
==================
This module changes HOW the chatbot answers based on the student's
emotional state detected by the webcam (from Tharaka's component).

If emotion detection is NOT available, the chatbot still works normally.
This is the "loose coupling" design - chatbot works with OR without emotion data.

Emotional States:
-----------------
- "understanding"  → Student is following well → Normal full explanation
- "confused"       → Student doesn't get it   → Simpler explanation + visuals
- "bored"          → Student is disengaged    → More engaging, fun tone
- "distracted"     → Student is not focused   → Very short, refocus answer
- "neutral"        → No emotion detected      → Normal explanation
"""



# RESPONSE TEMPLATES FOR EACH EMOTION STATE
# These are the "wrappers" added around the answer
# depending on how the student feels


EMOTION_TEMPLATES = {

    "confused": {
        "prefix": "Let me explain this in a simpler way 😊\n\n",
        "suffix": "\n\n💡 Tip: Read this slowly. If you still find it difficult, try asking me to give you an example!",
        "style": "simple",
        "tone": "gentle and very clear"
    },

    "bored": {
        "prefix": "Here's something interesting! 🌟\n\n",
        "suffix": "\n\n🎯 Did you know this is used in real life too? Want me to show you a real example?",
        "style": "engaging",
        "tone": "exciting and motivating"
    },

    "distracted": {
        "prefix": "👋 Hey! Let's focus for just a moment:\n\n",
        "suffix": "\n\n✅ That's the key point. Ready to continue?",
        "style": "brief",
        "tone": "short and direct"
    },

    "understanding": {
        "prefix": "",
        "suffix": "\n\n✨ Great job staying focused! Want to try a challenge question?",
        "style": "normal",
        "tone": "encouraging"
    },

    "neutral": {
        "prefix": "",
        "suffix": "",
        "style": "normal",
        "tone": "friendly and clear"
    }
}


# -------------------------------------------------------
# SIMPLIFIED EXPLANATIONS
# When student is confused, we simplify the answer
# These are simpler versions of complex terms
# -------------------------------------------------------

SIMPLIFICATION_MAP = {
    "database": "a digital filing cabinet that stores information",
    "algorithm": "a step-by-step set of instructions to solve a problem",
    "normalization": "organizing data in a database to remove repetition",
    "primary key": "a unique ID for each row in a database table",
    "foreign key": "a link connecting two database tables together",
    "CPU": "the brain of the computer that processes everything",
    "RAM": "temporary memory that stores what you are currently working on",
    "ROM": "permanent memory that stores the computer's startup instructions",
    "operating system": "software that manages all parts of the computer",
    "compiler": "a program that translates your code into computer language",
    "network": "a group of computers connected together to share information",
    "internet": "a giant worldwide network connecting millions of computers",
    "bandwidth": "how much data can travel through a connection per second",
    "firewall": "a security guard that blocks dangerous data from entering",
    "malware": "harmful software designed to damage your computer",
    "virus": "a program that copies itself and damages your computer",
    "DBMS": "software that helps you create and manage databases",
    "data": "raw facts and figures without any meaning on their own",
    "information": "processed data that has meaning and is useful",
    "ICT": "technology used to handle, store, and share information",
}


def adapt_response(answer, emotion_state, intent):
    """
    Main function - Takes an answer and wraps it with emotion-appropriate language.

    Parameters:
    -----------
    answer       : The answer found from the knowledge base
    emotion_state: The student's current emotion (confused/bored/distracted/understanding/neutral)
    intent       : Whether this is exam mode or learning mode

    Returns:
    --------
    A modified answer string that fits the student's emotional state
    """

    # If no emotion data received, use neutral
    if not emotion_state or emotion_state not in EMOTION_TEMPLATES:
        emotion_state = "neutral"

    # In exam mode, always give short answer regardless of emotion
    # (exam answers must be concise)
    if intent == "exam":
        return format_exam_answer(answer)

    # Get the template for this emotion
    template = EMOTION_TEMPLATES[emotion_state]

    # If student is confused, simplify the answer
    if emotion_state == "confused":
        answer = simplify_answer(answer)

    # If student is distracted, shorten the answer
    if emotion_state == "distracted":
        answer = shorten_answer(answer)

    # Build the final response
    final_response = template["prefix"] + answer + template["suffix"]

    return final_response


def format_exam_answer(answer):
    """
    Formats the answer as a clean exam-style response.
    Short, precise, ready to write in an exam paper.
    """
    # Take only the first 2 sentences for exam answers
    sentences = answer.split('.')
    short_answer = '. '.join(sentences[:2]).strip()
    if short_answer and not short_answer.endswith('.'):
        short_answer += '.'

    return f"📝 Exam Answer:\n\n{short_answer}"


def simplify_answer(answer):
    """
    Tries to make the answer simpler when student is confused.
    Replaces complex terms with simpler definitions.
    """
    simplified = answer

    # Replace complex terms with simpler ones
    for term, simple_version in SIMPLIFICATION_MAP.items():
        # Replace the term but keep it readable
        if term.lower() in simplified.lower():
            simplified = simplified.replace(
                term,
                f"{term} ({simple_version})"
            )

    return simplified


def shorten_answer(answer):
    """
    Returns only the first sentence when student is distracted.
    We want to bring their focus back with a short key point.
    """
    sentences = answer.split('.')
    if len(sentences) > 1:
        return sentences[0].strip() + '.'
    return answer


def get_visual_suggestion(topic, emotion_state):
    """
    Suggests visual content when student is confused.
    This connects to Mendis's Adaptive Content Subsystem.
    If that subsystem is not available, returns None gracefully.

    Returns a suggestion message about what visual to show.
    """

    # Only suggest visuals when confused or for learning mode
    if emotion_state not in ["confused", "understanding", "neutral"]:
        return None

    # Visual suggestions per topic keyword
    visual_map = {
        "database": "📊 Visual: Database table diagram",
        "network": "🌐 Visual: Network diagram showing connected computers",
        "cpu": "🖥️ Visual: CPU components diagram",
        "memory": "💾 Visual: Memory hierarchy diagram",
        "algorithm": "📋 Visual: Flowchart of algorithm steps",
        "normalization": "📊 Visual: Before and after normalization table",
        "computer": "🖥️ Visual: Computer components diagram",
        "internet": "🌐 Visual: How internet connects computers",
        "generation": "📅 Visual: Timeline of computer generations",
        "input": "⌨️ Visual: Common input devices",
        "output": "🖨️ Visual: Common output devices",
        "software": "💻 Visual: Types of software diagram",
        "hardware": "🔧 Visual: Hardware components layout",
    }

    topic_lower = topic.lower() if topic else ""

    for keyword, suggestion in visual_map.items():
        if keyword in topic_lower:
            return suggestion

    return None


def detect_emotion_from_text(text):
    """
    FALLBACK: If emotion detection subsystem (Tharaka's component) is not available,
    this function tries to detect emotion from the student's TEXT ITSELF.

    This keeps the chatbot working independently.
    """
    text_lower = text.lower()

    # Confusion signals in text
    confusion_words = [
        "don't understand", "dont understand", "confused", "confusing",
        "not clear", "unclear", "what does this mean", "i don't get",
        "i dont get", "hard to understand", "difficult", "help me",
        "explain again", "still don't understand"
    ]

    # Frustration/boredom signals
    boredom_words = [
        "boring", "bored", "this is hard", "too long", "too much",
        "complicated", "difficult", "not interested"
    ]

    # Check for confusion
    for word in confusion_words:
        if word in text_lower:
            return "confused"

    # Check for boredom
    for word in boredom_words:
        if word in text_lower:
            return "bored"

    # Default to neutral
    return "neutral"