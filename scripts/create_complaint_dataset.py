"""Script to generate the binary complaint detection dataset (data/complaint_dataset.csv).

Reuses all positive samples from data/dataset.csv as 'complaint',
and generates a diverse set of negative samples labeled as 'not_complaint'.
"""

import csv
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGINAL_DATASET = BASE_DIR / "data" / "dataset.csv"
OUTPUT_DATASET = BASE_DIR / "data" / "complaint_dataset.csv"

# Diverse categories of non-complaint texts
GREETINGS = [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night",
    "hey there", "hello there", "namaste", "hi judi", "hello assistant", "hey judi",
    "is anyone there", "hello how are you", "greetings", "hi bot", "hello bot",
    "what's up", "howdy", "salutations", "morning", "evening", "hi!", "hello!", "hey!"
]

SMALL_TALK = [
    "how are you", "how are you doing", "how is it going", "how's your day",
    "what is your name", "who are you", "who made you", "are you human", "are you an ai",
    "are you a robot", "what can you do", "tell me about yourself", "how do you work",
    "how's the weather today", "what is the weather like", "where do you live",
    "what are your features", "what are your capabilities", "tell me something interesting",
    "do you have feelings", "what is your purpose", "can you talk to me", "who created this system"
]

GRATITUDE_AND_CLOSURES = [
    "thanks", "thank you", "thanks a lot", "thank you so much", "thanks for your help",
    "thank you very much", "many thanks", "appreciate it", "i appreciate your help",
    "okay", "ok", "got it", "understood", "cool", "alright", "great", "sure", "no problem",
    "fine", "okay thanks", "ok thank you", "cool thanks", "alright got it",
    "bye", "goodbye", "see you", "see you later", "catch you later", "take care",
    "have a nice day", "have a great day", "good night and bye", "talk to you soon"
]

GENERAL_KNOWLEDGE = [
    "what is the capital of France", "what is the capital of India", "what is the capital of Japan",
    "how does photosynthesis work", "explain quantum physics", "who wrote Romeo and Juliet",
    "what is the speed of light", "why is the sky blue", "how do computers work",
    "what is python programming", "how far is the moon", "tell me about the solar system",
    "what is the largest ocean", "how many continents are there", "what is the currency of the UK",
    "who is the prime minister of India", "what is the tallest mountain in the world",
    "how many planets are in our solar system", "what is the boiling point of water",
    "who discovered gravity", "what is DNA", "explain theory of relativity"
]

MATH_AND_HOMEWORK = [
    "what is 2 + 2", "solve 5x + 3 = 18", "can you help me with my math homework",
    "how do you calculate the area of a circle", "what is the square root of 144",
    "what is 15 multiplied by 8", "write a short poem about nature", "give me a recipe for pasta",
    "translate hello to Spanish", "correct the grammar in this sentence",
    "what is a synonym for intelligent", "how to write a formal email",
    "can you summarize this paragraph", "give me some study tips", "how to prepare for exams"
]

ENTERTAINMENT_AND_JOKES = [
    "tell me a joke", "make me laugh", "do you know any funny jokes", "tell me another joke",
    "what is your favorite movie", "recommend a good book to read", "sing a song",
    "tell me a fun fact", "play a game with me", "do you like music",
    "who is the best football player", "what is your favorite food", "tell me a story",
    "do you know riddles", "give me a riddle to solve", "recommend some relaxing songs"
]

CASUAL_STATEMENTS = [
    "I am feeling happy today", "I love playing basketball", "I am going to college today",
    "I ate pizza for lunch", "my exam is tomorrow morning", "I am studying computer science",
    "today is a very sunny day", "I bought a new laptop yesterday", "I am learning how to drive",
    "I love watching movies on weekends", "the library is quiet today", "I had a cup of coffee",
    "I am excited for my vacation", "listening to music helps me relax", "I am doing my college assignment"
]

GENERAL_LEGAL_CURIOSITY = [
    "what is the constitution", "what is law", "define jurisprudence",
    "who is the chief justice of India", "what does the supreme court do",
    "how many articles are in the Indian constitution", "what is legal aid",
    "how does the judiciary system work", "what is a lawyer", "what is a judge",
    "tell me about law schools", "how to become an advocate in India"
]

SHORT_PHRASES_AND_TESTS = [
    "test", "testing", "test message", "testing 123", "hello?", "hi?", "anyone?",
    "yes", "no", "yeah", "nope", "yep", "nah", "hmm", "why", "what", "how",
    "ok", "k", "yo", "hey!", "pls", "help", "hello there bot"
]

def generate_not_complaint_samples():
    base_samples = (
        GREETINGS + SMALL_TALK + GRATITUDE_AND_CLOSURES +
        GENERAL_KNOWLEDGE + MATH_AND_HOMEWORK + ENTERTAINMENT_AND_JOKES +
        CASUAL_STATEMENTS + GENERAL_LEGAL_CURIOSITY + SHORT_PHRASES_AND_TESTS
    )
    
    unique_samples = set(s.strip() for s in base_samples if s.strip())
    
    # Generate natural variations
    variations = set()
    for s in unique_samples:
        variations.add(s)
        variations.add(s.lower())
        variations.add(s.capitalize())
        if not s.endswith(('.', '!', '?')):
            variations.add(s + '.')
            variations.add(s + '!')
            variations.add(s + '?')
            variations.add(s + ' :)')
            variations.add(s + ' please')
            variations.add('please ' + s)
    
    return sorted(list(variations))

def main():
    print(f"Reading original dataset from: {ORIGINAL_DATASET}")
    df_orig = pd.read_csv(ORIGINAL_DATASET)
    
    # 1. Prepare positive samples (complaint)
    complaint_rows = []
    for text in df_orig["text"].dropna():
        cleaned_text = str(text).strip()
        if cleaned_text:
            complaint_rows.append({"text": cleaned_text, "label": "complaint"})
    
    print(f"Found {len(complaint_rows)} complaint samples.")
    
    # 2. Prepare negative samples (not_complaint)
    not_complaint_samples = generate_not_complaint_samples()
    not_complaint_rows = [{"text": s, "label": "not_complaint"} for s in not_complaint_samples]
    print(f"Generated {len(not_complaint_rows)} not_complaint samples.")
    
    # 3. Combine and save
    all_rows = complaint_rows + not_complaint_rows
    df_binary = pd.DataFrame(all_rows).drop_duplicates(subset=["text"])
    
    OUTPUT_DATASET.parent.mkdir(parents=True, exist_ok=True)
    df_binary.to_csv(OUTPUT_DATASET, index=False, quoting=csv.QUOTE_MINIMAL)
    
    print(f"\nSaved binary dataset to: {OUTPUT_DATASET}")
    print(f"Total rows: {len(df_binary)}")
    print("Class distribution:")
    print(df_binary["label"].value_counts())

if __name__ == "__main__":
    main()
