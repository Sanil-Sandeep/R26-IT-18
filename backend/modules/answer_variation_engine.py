"""
answer_variation_engine.py
===========================
Generates multiple different versions of the same answer.

Same question + same emotion → STILL different answer per student.

How it works:
-------------
1. Takes base answer from knowledge base
2. Generates 6 different structural variations
3. Uses student_id hash to CONSISTENTLY pick one variation per student
   (Student A always gets variation 2, Student B always gets variation 5)
4. Emotion layer is applied on TOP of the variation

Result: 5 emotions × 6 variations = 30 possible unique answers per question
"""

import hashlib
import random


# -------------------------------------------------------
# EXAMPLE BANK
# Different real-world examples added to enrich answers
# -------------------------------------------------------
EXAMPLES_BANK = {
    "ict": [
        "Example: Online banking lets you transfer money from home using ICT.",
        "Example: Doctors use ICT to access patient records instantly.",
        "Example: Students use ICT to learn through online platforms like this one.",
        "Example: Supermarkets use ICT to manage stock and billing automatically.",
        "Example: Weather forecasting uses ICT to process millions of data points.",
    ],
    "data": [
        "Example: The number 25 is data. But '25 is Sanil's age' is information.",
        "Example: A list of exam scores is data. The class average calculated from it is information.",
        "Example: '38.5' is raw data. '38.5°C — the patient has a fever' is information.",
        "Example: Pixels in a photo are data. The image you see is information.",
        "Example: A barcode number is data. The product name and price it represents is information.",
    ],
    "database": [
        "Example: A school's student database stores names, grades and attendance.",
        "Example: Facebook uses a database to store billions of user profiles.",
        "Example: A hospital database stores patient names, diagnoses and medicines.",
        "Example: An online shop uses a database to track products and orders.",
        "Example: A library database stores book titles, authors and availability.",
    ],
    "network": [
        "Example: Your home WiFi is a small network connecting your devices.",
        "Example: A school network connects all computers in the lab to one printer.",
        "Example: The internet is the world's largest network.",
        "Example: ATM machines are connected through a bank's private network.",
        "Example: Online gaming connects players worldwide through a network.",
    ],
    "cpu": [
        "Example: When you open an app, the CPU processes the instructions to display it.",
        "Example: Playing a video game requires the CPU to calculate thousands of actions per second.",
        "Example: The CPU decides what happens when you press a key on your keyboard.",
        "Example: A smartphone CPU processes camera photos in milliseconds.",
        "Example: When you search Google, a CPU processes your query and finds results.",
    ],
    "software": [
        "Example: Microsoft Word is application software for writing documents.",
        "Example: Windows is system software that manages your computer.",
        "Example: A calculator app on your phone is utility software.",
        "Example: A school management system is custom software.",
        "Example: Antivirus programs are utility software that protect your computer.",
    ],
    "hardware": [
        "Example: The keyboard you type on is hardware.",
        "Example: Your computer screen is an output hardware device.",
        "Example: A USB flash drive is a storage hardware device.",
        "Example: The mouse is an input hardware device.",
        "Example: A printer is an output hardware device.",
    ],
    "algorithm": [
        "Example: A recipe is like an algorithm — step by step instructions to make food.",
        "Example: Traffic lights follow an algorithm to control vehicle flow.",
        "Example: Google uses algorithms to rank search results.",
        "Example: ATMs follow an algorithm to verify your PIN and dispense cash.",
        "Example: Sorting exam results from highest to lowest follows an algorithm.",
    ],
    "internet": [
        "Example: When you send a WhatsApp message, it travels through the internet.",
        "Example: Watching YouTube uses the internet to stream video to your device.",
        "Example: Online shopping connects buyers and sellers through the internet.",
        "Example: Video calls use the internet to send voice and video data.",
        "Example: Emails travel through the internet to reach recipients worldwide.",
    ],
    "memory": [
        "Example: RAM stores the document you are currently editing — it clears when you shut down.",
        "Example: ROM stores the startup instructions — it never changes.",
        "Example: A 16GB phone memory can store thousands of photos.",
        "Example: When you run too many apps, RAM fills up and your phone slows down.",
        "Example: Saving a file moves it from RAM (temporary) to storage (permanent).",
    ],
    "default": [
        "Example: This concept is widely used in modern computing systems.",
        "Example: This is one of the key topics in the O/L ICT syllabus.",
        "Example: Understanding this helps you answer both theory and practical questions.",
        "Example: This concept appears in almost every chapter of your ICT textbook.",
        "Example: Examiners frequently ask about this in O/L ICT papers.",
    ]
}

# -------------------------------------------------------
# DIFFERENT STRUCTURAL FORMATS
# Same content, different presentation
# -------------------------------------------------------

def get_variation_index(student_id, question):
    """
    Generates a consistent index (0-5) based on student_id.
    Same student always gets the same variation for same question.
    Different students get different variations.
    """
    # Create a unique key from student + question
    key = f"{student_id}_{question[:30]}"
    # Hash it to get a number
    hash_num = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return hash_num % 6  # Returns 0, 1, 2, 3, 4, or 5


def get_example(answer_text):
    """
    Finds the most relevant example for the given answer.
    """
    answer_lower = answer_text.lower()

    for keyword, examples in EXAMPLES_BANK.items():
        if keyword != 'default' and keyword in answer_lower:
            return random.choice(examples)

    return random.choice(EXAMPLES_BANK['default'])


def generate_variation(base_answer, student_id, question, variation_index=None):
    """
    Generates one of 6 structural variations of the answer.

    Parameters:
    -----------
    base_answer     : The original answer from the knowledge base
    student_id      : Used to consistently pick a variation
    question        : The original question (used for hashing)
    variation_index : Override the auto-selected variation (optional)

    Returns:
    --------
    A string — the answer in a specific structural format
    """

    # Get consistent variation index for this student
    if variation_index is None:
        variation_index = get_variation_index(student_id, question)

    # Get a relevant example
    example = get_example(base_answer)

    # Split answer into sentences
    sentences = [s.strip() for s in base_answer.split('.') if s.strip()]
    full = base_answer.strip()
    first = sentences[0] if sentences else full
    rest = '. '.join(sentences[1:]) if len(sentences) > 1 else ''

    # ---- 6 Different Structural Formats ----

    if variation_index == 0:
        # Format 0: Definition + Example + Key Point
        return (
            f"📌 Definition:\n"
            f"{full}\n\n"
            f"📎 {example}\n\n"
            f"🔑 Key Point: {first}."
        )

    elif variation_index == 1:
        # Format 1: Bullet point breakdown
        bullet_points = '\n'.join([f"  • {s}." for s in sentences[:4]])
        return (
            f"Here is the answer broken down:\n\n"
            f"{bullet_points}\n\n"
            f"📎 {example}"
        )

    elif variation_index == 2:
        # Format 2: Question → Answer → Why it matters
        why_matters = [
            "Understanding this helps you answer theory questions in your exam.",
            "This is a foundational concept that appears in many ICT topics.",
            "Knowing this will help you understand more advanced ICT topics.",
            "This is one of the most commonly asked topics in O/L ICT exams.",
            "Mastering this will give you a strong base for all ICT chapters.",
        ]
        return (
            f"❓ You asked about this — here is a clear explanation:\n\n"
            f"{full}\n\n"
            f"📎 {example}\n\n"
            f"💡 Why it matters: {random.choice(why_matters)}"
        )

    elif variation_index == 3:
        # Format 3: Summary box style
        return (
            f"┌─────────────────────────────┐\n"
            f"  ANSWER\n"
            f"└─────────────────────────────┘\n\n"
            f"{full}\n\n"
            f"┌─────────────────────────────┐\n"
            f"  REAL WORLD EXAMPLE\n"
            f"└─────────────────────────────┘\n\n"
            f"{example}"
        )

    elif variation_index == 4:
        # Format 4: Teach-back style — explains like talking to a friend
        teach_intros = [
            "Okay, let me explain this simply:",
            "Think of it this way:",
            "Here is the simplest way to understand it:",
            "Let me put it in plain words:",
            "The easiest way to think about this is:",
        ]
        return (
            f"💬 {random.choice(teach_intros)}\n\n"
            f"{full}\n\n"
            f"📎 {example}\n\n"
            f"👉 In short: {first}."
        )

    else:
        # Format 5: Numbered points + summary
        numbered = '\n'.join([f"  {i+1}. {s}." for i, s in enumerate(sentences[:4])])
        return (
            f"Here is everything you need to know:\n\n"
            f"{numbered}\n\n"
            f"📎 {example}\n\n"
            f"✅ Summary: {first}."
        )


def generate_all_variations(base_answer, question):
    """
    Returns all 6 variations of an answer.
    Useful for testing — shows you what different students will see.
    """
    variations = []
    for i in range(6):
        variation = generate_variation(base_answer, f"student_{i}", question, variation_index=i)
        variations.append({
            "variation": i,
            "student_example": f"student_{i}",
            "answer": variation
        })
    return variations
