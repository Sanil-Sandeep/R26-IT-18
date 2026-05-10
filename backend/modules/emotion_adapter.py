"""
emotion_adapter.py - UPDATED
==============================
Now combines:
1. Answer Variation Engine  → Different structure per student
2. Emotion Formatting       → Different style per emotion state

Result: Every student gets a uniquely formatted answer
"""

import random
from modules.answer_variation_engine import generate_variation


def adapt_response(answer, emotion_state, intent, difficulty=1,
                   student_id="default", question=""):
    """
    Main function — generates a unique answer per student per emotion.

    Parameters:
    -----------
    answer       : Base answer from knowledge base
    emotion_state: confused / bored / distracted / understanding / neutral
    intent       : exam / learning
    difficulty   : 1 / 2 / 3
    student_id   : Unique per student — determines variation
    question     : Original question — used in hashing
    """

    if not emotion_state or emotion_state not in [
        'confused', 'bored', 'distracted', 'understanding', 'neutral'
    ]:
        emotion_state = 'neutral'

    # Exam mode — always short, no variation needed
    if intent == 'exam':
        return format_exam_answer(answer)

    # Step 1: Generate the student-specific variation of the answer
    varied_answer = generate_variation(answer, student_id, question)

    # Step 2: Wrap with emotion-specific formatting
    if emotion_state == 'confused':
        return format_confused(varied_answer, answer)
    elif emotion_state == 'bored':
        return format_bored(varied_answer)
    elif emotion_state == 'distracted':
        return format_distracted(answer)  # Keep short — just one sentence
    elif emotion_state == 'understanding':
        return format_understanding(varied_answer, difficulty)
    else:
        return format_neutral(varied_answer)


def format_exam_answer(answer):
    sentences = [s.strip() for s in answer.split('.') if s.strip()]
    short = sentences[0] if sentences else answer
    return (
        "📝 EXAM ANSWER\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{short}.\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✏️ Short and precise — ready for your exam paper."
    )


def format_confused(varied_answer, original_answer):
    sentences = [s.strip() for s in original_answer.split('.') if s.strip()]
    key = sentences[0] if sentences else original_answer

    analogies = [
        "Think of it like sorting your school bag — everything has its place.",
        "Imagine it like a library — things stored so you can find them easily.",
        "Think of it like your phone contacts — stored, organized, searchable.",
        "It is like a well-organized filing cabinet in an office.",
        "Think of it like a recipe book — information stored in a useful way.",
    ]

    return (
        "😊 NO WORRIES — Let me break this down simply!\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"💡 ANALOGY: {random.choice(analogies)}\n\n"
        f"{varied_answer}\n\n"
        f"🌟 MOST IMPORTANT POINT:\n"
        f"   → {key}.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔁 Still confused? Type: 'give me another example'"
    )


def format_bored(varied_answer):
    fun_facts = [
        "🤯 FUN FACT: Google processes 8.5 BILLION searches per day using these concepts!",
        "🚀 FUN FACT: NASA uses these ideas to manage space mission data!",
        "💰 FUN FACT: Banks process millions of transactions per second with this!",
        "🎮 FUN FACT: Video games use this to save your progress and run game logic!",
        "🏥 FUN FACT: Hospitals store millions of patient records using this!",
    ]

    return (
        "🌟 HEY — THIS IS ACTUALLY FASCINATING!\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(fun_facts)}\n\n"
        f"{varied_answer}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 CHALLENGE: Can you think of another real-world use? Type it!"
    )


def format_distracted(answer):
    sentences = [s.strip() for s in answer.split('.') if s.strip()]
    key = sentences[0] if sentences else answer

    return (
        "👋 HEY! Focus — Just ONE thing right now:\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⭐ {key}.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "✅ Got it? Type 'tell me more' when ready for the full answer."
    )


def format_understanding(varied_answer, difficulty=1):
    if difficulty >= 3:
        deeper = [
            "🔬 THINK DEEPER: How does this connect to databases and DBMS?",
            "🔬 THINK DEEPER: What problems would occur if this did not exist?",
            "🔬 THINK DEEPER: How would a software engineer use this?",
        ]
        return (
            "🏆 EXCELLENT! Here is the ADVANCED explanation:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{varied_answer}\n\n"
            f"{random.choice(deeper)}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🏆 You are at ADVANCED LEVEL — try asking a harder question!"
        )
    elif difficulty == 2:
        return (
            "👍 GREAT! Here is a detailed explanation:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{varied_answer}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💪 You are doing great — keep going!"
        )
    else:
        return (
            "✨ HERE IS A CLEAR EXPLANATION:\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{varied_answer}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 TIP: Remember the key definition first, then the details."
        )


def format_neutral(varied_answer):
    intros = [
        "📚 HERE IS YOUR ANSWER:",
        "💬 GREAT QUESTION! HERE IS THE ANSWER:",
        "📖 LET ME EXPLAIN:",
        "🎓 HERE IS THE ICT EXPLANATION:",
    ]
    return (
        f"{random.choice(intros)}\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{varied_answer}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 Try changing your emotion above to get a different style!"
    )


def get_visual_suggestion(topic, emotion_state):
    if emotion_state not in ['confused', 'understanding', 'neutral']:
        return None

    visual_map = {
        'database':      '📊 Visual: Database table structure diagram',
        'network':       '🌐 Visual: Network topology diagram',
        'cpu':           '🖥️ Visual: CPU components and data flow',
        'memory':        '💾 Visual: Memory hierarchy (RAM, ROM, Cache)',
        'algorithm':     '📋 Visual: Algorithm flowchart',
        'normalization': '📊 Visual: Before/After normalization table',
        'computer':      '🖥️ Visual: Computer system components',
        'internet':      '🌐 Visual: How the internet connects devices',
        'generation':    '📅 Visual: Timeline of computer generations',
        'input':         '⌨️ Visual: Input devices diagram',
        'output':        '🖨️ Visual: Output devices diagram',
        'software':      '💻 Visual: Types of software tree diagram',
        'hardware':      '🔧 Visual: Hardware components layout',
        'ict':           '📡 Visual: ICT applications in society',
    }

    topic_lower = (topic or '').lower()
    for keyword, suggestion in visual_map.items():
        if keyword in topic_lower:
            return suggestion
    return None


def detect_emotion_from_text(text):
    text_lower = text.lower()

    confusion_words = [
        "don't understand", "dont understand", "confused", "confusing",
        "not clear", "unclear", "i don't get", "i dont get",
        "hard", "difficult", "help me", "explain again",
        "what does this mean", "still don't understand"
    ]
    boredom_words = [
        "boring", "bored", "too long", "too much",
        "not interested", "whatever"
    ]

    for word in confusion_words:
        if word in text_lower:
            return "confused"
    for word in boredom_words:
        if word in text_lower:
            return "bored"
    return "neutral"
