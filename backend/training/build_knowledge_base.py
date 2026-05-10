
# This script takes the Q&A dataset and converts every question
# into a "vector" (a list of numbers that represents its meaning).

# Then it builds a FAISS index — think of it like a super smart search engine.
# When a student asks a question, FAISS instantly finds the most similar
# question in the dataset and returns that answer.

# This is the "training" step — after this, the chatbot knows everything
# from your Excel files.


import os
import json
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


# SETTINGS

DATASET_FILE = os.path.join("backend", "data", "full_dataset.json")
MODELS_FOLDER = os.path.join("backend", "models")
INDEX_FILE = os.path.join(MODELS_FOLDER, "faiss_index.pkl")
METADATA_FILE = os.path.join(MODELS_FOLDER, "qa_metadata.json")
EMBEDDINGS_FILE = os.path.join(MODELS_FOLDER, "embeddings.npy")

# The AI model we use to understand sentence meaning
# This model runs 100% locally on your computer - no internet needed after first download
MODEL_NAME = "all-MiniLM-L6-v2"


def load_dataset(file_path):
    """
    Loads the Q&A dataset we created in prepare_dataset.py
    """
    print(f"Loading dataset from: {file_path}")
    
    if not os.path.exists(file_path):
        print("ERROR: Dataset file not found!")
        print("Please run prepare_dataset.py first.")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    print(f"Loaded {dataset['total_count']} Q&A pairs")
    return dataset


def load_sentence_model():
    """
    Loads the sentence transformer model.
    
    What is a Sentence Transformer?
    --------------------------------
    It's an AI model that reads a sentence and converts it into a list of
    384 numbers (called a "vector" or "embedding"). 
    
    Two sentences that MEAN the same thing will have SIMILAR numbers,
    even if they use different words.
    
    Example:
    "What is ICT?" → [0.23, -0.15, 0.87, ...] (384 numbers)
    "Define ICT"   → [0.24, -0.14, 0.85, ...] (very similar numbers!)
    
    This is how the chatbot understands questions even with different wording.
    """
    print(f"\nLoading AI sentence model: {MODEL_NAME}")
    print("(This may take a moment on first run - it downloads the model)")
    
    model = SentenceTransformer(MODEL_NAME)
    
    print("Model loaded successfully!")
    return model


def create_embeddings(model, qa_pairs):
    """
    Converts all questions in the dataset into vectors (numbers).
    
    Think of it like translating every question into a secret code
    that captures the MEANING of the question.
    """
    print(f"\nConverting {len(qa_pairs)} questions into AI vectors...")
    print("(This may take a minute...)")
    
    # Extract just the questions
    questions = [pair['question'] for pair in qa_pairs]
    
    # Convert all questions to vectors at once
    # show_progress_bar=True shows a loading bar in the terminal
    embeddings = model.encode(
        questions,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True  # Makes similarity search more accurate
    )
    
    print(f"\nCreated {len(embeddings)} vectors")
    print(f"Each vector has {embeddings.shape[1]} numbers")
    return embeddings


def build_faiss_index(embeddings):
    """
    Builds a FAISS index from the vectors.
    
    What is FAISS?
    --------------
    FAISS is like a super-fast filing cabinet. Instead of searching through
    all 1000+ questions one by one, FAISS can instantly find the most
    similar question in milliseconds.
    
    It works by organizing vectors in a smart way so searching is very fast.
    """
    try:
        import faiss
    except ImportError:
        print("ERROR: faiss not installed. Run: pip install faiss-cpu")
        return None
    
    print("\nBuilding FAISS search index...")
    
    # Get the size of each vector (384 for this model)
    dimension = embeddings.shape[1]
    
    # Create a FAISS index that uses cosine similarity
    # IndexFlatIP = Flat Index with Inner Product (dot product of normalized vectors = cosine similarity)
    index = faiss.IndexFlatIP(dimension)
    
    # Add all our vectors to the index
    index.add(embeddings.astype(np.float32))
    
    print(f"FAISS index built with {index.ntotal} vectors")
    return index


def save_everything(index, qa_pairs, embeddings):
    """
    Saves the FAISS index and all Q&A data to the models folder.
    These files are what the chatbot loads when it starts up.
    """
    
    # Create the models folder if it doesn't exist
    os.makedirs(MODELS_FOLDER, exist_ok=True)
    
    print(f"\nSaving knowledge base to: {MODELS_FOLDER}")
    
    # Save the FAISS index
    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(index, f)
    print(f"  Saved FAISS index: {INDEX_FILE}")
    
    # Save the Q&A metadata (questions, answers, sources)
    metadata = {
        "total": len(qa_pairs),
        "qa_pairs": qa_pairs
    }
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"  Saved Q&A metadata: {METADATA_FILE}")
    
    # Save the embeddings (vectors)
    np.save(EMBEDDINGS_FILE, embeddings)
    print(f"  Saved embeddings: {EMBEDDINGS_FILE}")
    
    print("\nAll files saved successfully!")


def test_search(index, qa_pairs, model):
    """
    Tests the knowledge base with a sample question to make sure it works.
    This is like a quick check to confirm everything is working.
    """
    print("\n" + "="*50)
    print("TESTING THE KNOWLEDGE BASE")
    print("="*50)
    
    test_questions = [
        "What is data?",
        "Who invented the computer?",
        "What does ICT stand for?"
    ]
    
    for test_q in test_questions:
        print(f"\nTest question: '{test_q}'")
        
        # Convert the test question to a vector
        query_vector = model.encode([test_q], normalize_embeddings=True)
        
        # Search for the 1 most similar question
        distances, indices = index.search(query_vector.astype(np.float32), k=1)
        
        best_match_index = indices[0][0]
        confidence = float(distances[0][0])
        
        matched_question = qa_pairs[best_match_index]['question']
        matched_answer = qa_pairs[best_match_index]['answer']
        
        print(f"  Best match: '{matched_question}'")
        print(f"  Answer: '{matched_answer[:100]}...'")
        print(f"  Confidence: {confidence:.2%}")



# MAIN

if __name__ == "__main__":
    print("="*50)
    print("ICT CHATBOT - Building Knowledge Base")
    print("="*50)
    
    # Step 1: Load the dataset
    dataset = load_dataset(DATASET_FILE)
    if not dataset:
        exit()
    
    qa_pairs = dataset['qa_pairs']
    
    # Step 2: Load the AI sentence model
    model = load_sentence_model()
    
    # Step 3: Convert questions to vectors
    embeddings = create_embeddings(model, qa_pairs)
    
    # Step 4: Build the FAISS search index
    index = build_faiss_index(embeddings)
    if not index:
        exit()
    
    # Step 5: Save everything
    save_everything(index, qa_pairs, embeddings)
    
    # Step 6: Test it works
    test_search(index, qa_pairs, model)
    
    print("\n" + "="*50)
    print("Knowledge base is ready!")
    print("Next step: Run train_intent_classifier.py")
    print("="*50)