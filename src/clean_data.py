'''import os
import json
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(base_dir, "data", "reddit_data")
OUTPUT_DIR = os.path.join(base_dir, "data", "filtered_comments")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def is_opinion_comment(comment_text, threshold=0.5):
    sentiment = sia.polarity_scores(comment_text)
    compound = sentiment['compound']
    if abs(compound) >= threshold:
        return True
    else:
        return False


def filter_comments(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    filtered_comments = []
    for comments in data:
        if is_opinion_comment(comments):
            filtered_comments.append(comments)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_comments, f, indent=4)


def main():
    json_files = [file for file in os.listdir(INPUT_DIR) if file.endswith(".json")]

    for json_file in tqdm(json_files):
        input_path = os.path.join(INPUT_DIR, json_file)
        output_path = os.path.join(OUTPUT_DIR, json_file)

        filter_comments(input_path, output_path)



if __name__ == "__main__":
    main()
'''

import os
import json
from tqdm import tqdm
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

sia = SentimentIntensityAnalyzer()

# Classification model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Relevant topics
grammy_keywords = ["Grammy", "Grammys", "Best New Artist", "Record of the Year", "Album of the Year"]
artist_keywords = [
    "Kendrick Lamar", "Taylor Swift", "Beyonce", "Billie Eilish", "The Beatles", "Sabrina Carpenter",
    "Charli XCX", "Chappell Roan", "Andre 3000", "Jacob Collier", "Shaboozey", "Lady Gaga",
    "Bruno Mars", "Benson Boone", "Doechii", "Khruangbin", "Raye", "Teddy Swims"
]

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(base_dir, "data", "reddit_data")
OUTPUT_DIR = os.path.join(base_dir, "data", "filtered_comments")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Check if a comment expresses an opinion
def is_opinion_comment(comment_text, threshold=0.20):
    sentiment = sia.polarity_scores(comment_text)
    return abs(sentiment['compound']) >= threshold


# Check if the comment is relevant using BERT
def is_relevant_comment(comment_text):
    labels = ["Grammy Awards", "Music Artist", "Unrelated"]
    result = classifier(comment_text, labels)
    return result['labels'][0] in ["Grammy Awards", "Music Artist"]


# Check if the comment contains artist references
def contains_artist(comment_text):
    comment_lower = comment_text.lower()
    has_artist = any(artist.lower() in comment_lower for artist in artist_keywords)
    return has_artist


# Filter comments
def filter_comments(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    data = data[:250]  # Limit to first 250 comments for testing

    filtered_comments = []
    for i, comment in enumerate(data):
        print(f"\nProcessing comment {i + 1}/{len(data)}: {comment[:100]}...")  # Show first 100 chars for reference

        opinion_check = is_opinion_comment(comment)
        relevance_check = is_relevant_comment(comment)
        keyword_check = contains_artist(comment)

        print(f"  Sentiment Pass: {opinion_check}")
        print(f"  Relevance Pass: {relevance_check}")
        print(f"  Keyword Match: {keyword_check}")

        if opinion_check and relevance_check and keyword_check:
            filtered_comments.append(comment)
        else:
            print("Comment filtered out.")

    print(f"\nTotal comments passing all filters: {len(filtered_comments)}/{len(data)}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_comments, f, indent=4)


def main():
    json_files = [file for file in os.listdir(INPUT_DIR) if file.endswith(".json")]

    for json_file in tqdm(json_files):
        print(f"\nProcessing file: {json_file}")
        input_path = os.path.join(INPUT_DIR, json_file)
        output_path = os.path.join(OUTPUT_DIR, json_file)
        filter_comments(input_path, output_path)


if __name__ == "__main__":
    main()
