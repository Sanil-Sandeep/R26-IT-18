"""
train_intent_classifier.py
===========================
This script trains a classifier that detects whether a student is:
- In LEARNING MODE  → wants a full, clear explanation
- In EXAM MODE      → wants a short, exam-style answer

How it works:
1. We create a set of example sentences labeled as "learning" or "exam"
2. We convert sentences to numbers using TF-IDF
3. We train a Logistic Regression model on those numbers
4. We save the trained model so the chatbot can use it

"""

import os
import pickle
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score



# SETTINGS

MODELS_FOLDER = os.path.join("backend", "models")
INTENT_MODEL_FILE = os.path.join(MODELS_FOLDER, "intent_classifier.pkl")
INTENT_LABELS_FILE = os.path.join(MODELS_FOLDER, "intent_labels.json")



# TRAINING DATA
# These are example sentences we use to TEACH the classifier
# "exam" = student is studying for exam, wants short answer
# "learning" = student wants to understand deeply

TRAINING_DATA = [

    # ---- EXAM MODE examples ----
    # Keywords: define, state, list, mention, 2 marks, 4 marks, marks, exam, briefly
    ("define database", "exam"),
    ("define ICT", "exam"),
    ("define data", "exam"),
    ("define information", "exam"),
    ("define hardware", "exam"),
    ("define software", "exam"),
    ("define network", "exam"),
    ("define operating system", "exam"),
    ("define algorithm", "exam"),
    ("define internet", "exam"),
    ("define input device", "exam"),
    ("define output device", "exam"),
    ("define memory", "exam"),
    ("define CPU", "exam"),
    ("state two uses of ICT", "exam"),
    ("state three advantages of computers", "exam"),
    ("state the function of CPU", "exam"),
    ("list four input devices", "exam"),
    ("list three output devices", "exam"),
    ("list two types of software", "exam"),
    ("list the generations of computers", "exam"),
    ("mention two uses of internet", "exam"),
    ("mention three storage devices", "exam"),
    ("what is database 2 marks", "exam"),
    ("what is ICT 4 marks", "exam"),
    ("what is a network for 2 marks", "exam"),
    ("what is RAM for exam", "exam"),
    ("what is ROM for exam", "exam"),
    ("answer for exam what is CPU", "exam"),
    ("briefly explain what is data", "exam"),
    ("briefly describe the internet", "exam"),
    ("brief definition of software", "exam"),
    ("short answer for what is hardware", "exam"),
    ("give a short definition of algorithm", "exam"),
    ("exam question define operating system", "exam"),
    ("this is for my exam what is a compiler", "exam"),
    ("for 2 marks what is normalization", "exam"),
    ("name two input devices", "exam"),
    ("name three types of memory", "exam"),
    ("name the parts of a computer", "exam"),
    ("write short note on ICT", "exam"),
    ("write a short note on computer memory", "exam"),
    ("write the definition of internet", "exam"),
    ("give the definition of data", "exam"),
    ("give definition of information system", "exam"),
    ("what does ICT stand for", "exam"),
    ("what does CPU stand for", "exam"),
    ("what does RAM stand for", "exam"),
    ("what does ROM stand for", "exam"),
    ("what is the full form of ICT", "exam"),
    ("exam answer for types of computers", "exam"),
    ("short note on computer generations", "exam"),
    ("2 mark answer for what is software", "exam"),
    ("4 mark question explain input devices", "exam"),
    ("answer in brief about network", "exam"),
    ("define the term data communication", "exam"),
    ("define firewall", "exam"),
    ("define malware", "exam"),
    ("define virus", "exam"),
    ("define primary key", "exam"),
    ("define foreign key", "exam"),
    ("define normalization", "exam"),
    ("define DBMS", "exam"),
    ("state what is meant by database", "exam"),
    ("state the meaning of ICT", "exam"),

    # ---- LEARNING MODE examples ----
    # Keywords: explain, understand, how does, why, help me, tell me more,
    #           i dont understand, can you, what happens, show me
    ("explain how a database works", "learning"),
    ("explain what ICT is used for", "learning"),
    ("explain how the internet works", "learning"),
    ("explain computer generations in detail", "learning"),
    ("explain the difference between RAM and ROM", "learning"),
    ("explain how a CPU processes data", "learning"),
    ("explain types of software with examples", "learning"),
    ("explain what happens when we type on keyboard", "learning"),
    ("help me understand what a network is", "learning"),
    ("help me understand normalization", "learning"),
    ("help me understand how computers work", "learning"),
    ("help me understand data and information", "learning"),
    ("i dont understand what is algorithm", "learning"),
    ("i dont understand how internet works", "learning"),
    ("i dont understand normalization", "learning"),
    ("i do not understand what DBMS is", "learning"),
    ("can you explain what ICT is", "learning"),
    ("can you explain how a database works", "learning"),
    ("can you explain what a virus does", "learning"),
    ("can you explain types of computers", "learning"),
    ("can you tell me more about memory", "learning"),
    ("can you tell me more about networking", "learning"),
    ("tell me more about computer hardware", "learning"),
    ("tell me more about software types", "learning"),
    ("how does a computer work", "learning"),
    ("how does the internet connect computers", "learning"),
    ("how does RAM work in a computer", "learning"),
    ("how does a compiler work", "learning"),
    ("how does normalization help databases", "learning"),
    ("how does a firewall protect computers", "learning"),
    ("why do we use databases", "learning"),
    ("why is ICT important in education", "learning"),
    ("why do computers need an operating system", "learning"),
    ("why is normalization important", "learning"),
    ("why do we need primary keys", "learning"),
    ("what happens when a computer gets a virus", "learning"),
    ("what is the difference between data and information", "learning"),
    ("what is the difference between hardware and software", "learning"),
    ("what is the difference between RAM and ROM", "learning"),
    ("what are the uses of ICT in daily life", "learning"),
    ("show me how database works", "learning"),
    ("show me an example of normalization", "learning"),
    ("teach me about computer networks", "learning"),
    ("i want to learn about internet", "learning"),
    ("i want to understand what ICT is", "learning"),
    ("i am confused about normalization", "learning"),
    ("i am confused about what a database is", "learning"),
    ("please explain data communication to me", "learning"),
    ("describe in detail how computers evolved", "learning"),
    ("give me a detailed explanation of ICT", "learning"),
    ("give me examples of input devices", "learning"),
    ("give me examples of how ICT is used in health", "learning"),
    ("what are the advantages of using computers", "learning"),
    ("what are the disadvantages of internet", "learning"),
    ("how are computers used in hospitals", "learning"),
    ("what is ICT and how is it used in schools", "learning"),
    ("walk me through how data is stored", "learning"),
    ("break down what normalization means", "learning"),
]


def prepare_data(training_data):
    """
    Splits the training data into:
    - X = the sentences (what we use to learn from)
    - y = the labels (what we want to predict: "exam" or "learning")
    """
    X = [item[0] for item in training_data]   # Sentences
    y = [item[1] for item in training_data]   # Labels
    return X, y


def train_classifier(X, y):
    """
    Trains the intent classifier.

    What is TF-IDF?
    ---------------
    TF-IDF converts sentences into numbers based on which words appear
    and how important those words are.
    Example: "define database" → word "define" gets high weight
             "explain how database works" → "explain" and "how" get high weight

    What is Logistic Regression?
    ----------------------------
    A simple but very effective machine learning model.
    It learns from examples and can then predict labels for new sentences.

    What is a Pipeline?
    -------------------
    Combines TF-IDF + Logistic Regression into one step so we can
    easily use it later.
    """

    print("\nTraining the intent classifier...")

    # Split data: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples:  {len(X_test)}")

    # Create the pipeline: TF-IDF → Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 3),    # Look at 1, 2, and 3 word combinations
            max_features=5000,     # Use top 5000 most useful word combinations
            lowercase=True,        # Treat "Define" and "define" the same
            strip_accents='unicode'
        )),
        ('classifier', LogisticRegression(
            max_iter=1000,
            random_state=42,
            C=1.0
        ))
    ])

    # Train the model
    pipeline.fit(X_train, y_train)

    # Test how accurate it is
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"\n  Training complete!")
    print(f"  Accuracy: {accuracy:.2%}")
    print("\nDetailed Report:")
    print(classification_report(y_test, y_pred))

    return pipeline


def save_model(pipeline):
    """
    Saves the trained model to a file so the chatbot can load it later.
    """
    os.makedirs(MODELS_FOLDER, exist_ok=True)

    # Save the trained model
    with open(INTENT_MODEL_FILE, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"  Intent classifier saved: {INTENT_MODEL_FILE}")

    # Save the label names
    labels = {"labels": ["exam", "learning"], "descriptions": {
        "exam": "Student wants a short exam-style answer",
        "learning": "Student wants a detailed explanation"
    }}
    with open(INTENT_LABELS_FILE, 'w') as f:
        json.dump(labels, f, indent=2)
    print(f"  Labels saved: {INTENT_LABELS_FILE}")


def test_classifier(pipeline):
    """
    Tests the classifier with some example questions.
    This shows you how the chatbot will detect intent.
    """
    print("\n" + "="*50)
    print("TESTING THE INTENT CLASSIFIER")
    print("="*50)

    test_questions = [
        "define database",
        "explain how a database works",
        "what is ICT 2 marks",
        "help me understand what ICT is",
        "list three input devices",
        "how does the internet work",
        "state the function of CPU",
        "i dont understand normalization",
        "briefly explain what is RAM",
        "why do we use operating systems",
    ]

    print(f"\n{'Question':<45} {'Detected Intent':<15} {'Confidence'}")
    print("-" * 75)

    for question in test_questions:
        prediction = pipeline.predict([question])[0]
        probability = pipeline.predict_proba([question])[0]
        confidence = max(probability)

        # Emoji to make it easier to read
        emoji = "📝 EXAM" if prediction == "exam" else "📚 LEARN"
        print(f"{question:<45} {emoji:<15} {confidence:.2%}")


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("ICT CHATBOT - Training Intent Classifier")
    print("=" * 50)

    # Step 1: Prepare data
    X, y = prepare_data(TRAINING_DATA)
    print(f"\nTotal training examples: {len(X)}")
    print(f"  Exam mode examples:     {y.count('exam')}")
    print(f"  Learning mode examples: {y.count('learning')}")

    # Step 2: Train the model
    pipeline = train_classifier(X, y)

    # Step 3: Save the model
    print("\nSaving model...")
    save_model(pipeline)

    # Step 4: Test it
    test_classifier(pipeline)

    print("\n" + "="*50)
    print("Intent Classifier is ready!")
    print("Next step: Build the Chatbot Engine")
    print("="*50)