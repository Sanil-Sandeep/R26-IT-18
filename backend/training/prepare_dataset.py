
# This script reads ALL your Excel Q&A files from the qa_dataset folder,
# combines them into one big dataset, and saves it as a JSON file.

# Think of this like a librarian collecting all the books and making one master list.

import os
import json
import pandas as pd


# SETTINGS - paths to your folders

QA_FOLDER = os.path.join("backend", "data", "qa_dataset")   # Where your Excel files are
OUTPUT_FOLDER = os.path.join("backend", "data")              # Where we save the result
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "full_dataset.json")  # The final combined file


def load_all_excel_files(folder_path):
    """
    This function opens every Excel file in your qa_dataset folder
    and reads the Question and Answer columns.
    
    It returns a list like:
    [
        {"question": "What is data?", "answer": "Data is...", "source": "Chapter1"},
        {"question": "What is ICT?",  "answer": "ICT stands for...", "source": "Chapter2"},
        ...
    ]
    """
    
    all_qa_pairs = []   # This will hold all our Q&A pairs
    
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"ERROR: Folder not found: {folder_path}")
        print("Make sure your Excel files are in backend/data/qa_dataset/")
        return []
    
    # Get list of all Excel files in the folder
    excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]
    
    if len(excel_files) == 0:
        print("ERROR: No Excel files found in the qa_dataset folder!")
        print(f"Looking in: {folder_path}")
        return []
    
    print(f"\nFound {len(excel_files)} Excel file(s):")
    
    # Loop through each Excel file one by one
    for filename in excel_files:
        file_path = os.path.join(folder_path, filename)
        print(f"  Reading: {filename}...")
        
        try:
            # Read the Excel file using pandas
            df = pd.read_excel(file_path)
            
            # Check if it has 'Question' and 'Answer' columns
            if 'Question' not in df.columns or 'Answer' not in df.columns:
                print(f"    WARNING: {filename} does not have 'Question' and 'Answer' columns. Skipping.")
                continue
            
            # Remove any empty rows
            df = df.dropna(subset=['Question', 'Answer'])
            
            # Get the chapter name from the filename (e.g. "ICT_Chapter1_QA" -> "Chapter1")
            source_name = filename.replace('.xlsx', '').replace('.xls', '')
            
            # Add each Q&A pair to our list
            for index, row in df.iterrows():
                question = str(row['Question']).strip()
                answer = str(row['Answer']).strip()
                
                # Skip empty questions or answers
                if question and answer and question != 'nan' and answer != 'nan':
                    all_qa_pairs.append({
                        "id": len(all_qa_pairs),          # Unique number for each Q&A
                        "question": question,              # The question
                        "answer": answer,                  # The answer
                        "source": source_name,            # Which file it came from
                        "topic": extract_topic(source_name)  # The topic/chapter
                    })
            
            print(f"    Loaded {len(df)} Q&A pairs from {filename}")
        
        except Exception as e:
            print(f"    ERROR reading {filename}: {e}")
    
    return all_qa_pairs


def extract_topic(source_name):
    """
    Extracts a clean topic name from the filename.
    Example: "ICT_Chapter1_QA" → "Chapter 1"
             "ICT_Chapter5_QA" → "Chapter 5"
    """
    # Try to find chapter number in the filename
    import re
    match = re.search(r'[Cc]hapter(\d+)', source_name)
    if match:
        return f"Chapter {match.group(1)}"
    return source_name  # Return the full name if no chapter found


def save_dataset(qa_pairs, output_file):
    """
    Saves all Q&A pairs into a single JSON file.
    JSON is like a structured list that Python can easily read back later.
    """
    
    # Create the dataset dictionary with summary info
    dataset = {
        "total_count": len(qa_pairs),
        "description": "ICT O/L Chatbot Knowledge Base - Combined Q&A Dataset",
        "qa_pairs": qa_pairs
    }
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\nDataset saved to: {output_file}")


def show_summary(qa_pairs):
    """
    Prints a summary of what was loaded - useful to check everything worked.
    """
    print("\n" + "="*50)
    print("DATASET SUMMARY")
    print("="*50)
    print(f"Total Q&A pairs loaded: {len(qa_pairs)}")
    
    # Count by topic/chapter
    topics = {}
    for pair in qa_pairs:
        topic = pair['topic']
        topics[topic] = topics.get(topic, 0) + 1
    
    print("\nBreakdown by Chapter:")
    for topic, count in sorted(topics.items()):
        print(f"  {topic}: {count} questions")
    
    # Show 3 sample Q&A pairs as a preview
    print("\nSample Q&A pairs (first 3):")
    for pair in qa_pairs[:3]:
        print(f"\n  Q: {pair['question'][:80]}...")
        print(f"  A: {pair['answer'][:80]}...")
        print(f"  Source: {pair['source']}")
    
    print("\n" + "="*50)



# MAIN - This runs when you execute the script

if __name__ == "__main__":
    print("="*50)
    print("ICT CHATBOT - Dataset Preparation")
    print("="*50)
    print(f"\nLooking for Excel files in: {QA_FOLDER}")
    
    # Step 1: Load all Excel files
    qa_pairs = load_all_excel_files(QA_FOLDER)
    
    if len(qa_pairs) == 0:
        print("\nNo data was loaded. Please check your Excel files and try again.")
        exit()
    
    # Step 2: Show summary
    show_summary(qa_pairs)
    
    # Step 3: Save combined dataset
    save_dataset(qa_pairs, OUTPUT_FILE)
    
    print("\nDone! Your dataset is ready.")
    print(f"Next step: Run build_knowledge_base.py to train the AI model.")