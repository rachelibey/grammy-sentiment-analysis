# Grammy Sentiment Analysis

## Overview
This project analyzes listener sentiment toward Grammy-nominated artists and compares public opinion with actual Grammy outcomes. It scrapes Reddit discussions, filters opinionated and relevant comments using AI/ML, and performs sentiment analysis to determine audience reactions.

## Features
- **Reddit Web Scraping**: Extracts Grammy-related comments from Reddit.
- **Sentiment Analysis**: Uses VADER (or optionally BERT) to classify opinionated comments.
- **Relevance Filtering**: Ensures comments mention both Grammy-related terms and artist names.
- **Data Processing & Storage**: Stores filtered comments in structured JSON files.

## Installation
### Prerequisites
Ensure you have **Python 3.10+** installed. Use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate   # On Windows, use 'venv\Scripts\activate'
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Scrape Reddit Data
```bash
python src/scrape_reddit.py
```
This will retrieve Reddit comments and store them in `data/reddit_data/`.

### 2. Filter Opinionated & Relevant Comments
```bash
python src/filter_comments.py
```
This step processes the raw data and saves filtered comments in `data/filtered_comments/`.

### 3. Analyze Sentiment
```bash
python src/analyze_sentiment.py
```
This script performs sentiment analysis on the filtered comments.

## Configuration
- Modify the **artist list** and **Grammy keywords** in `filter_comments.py` to customize the filtering criteria.
- Adjust the **sentiment threshold** (`default: 0.2`) in `is_opinion_comment()` to change the sensitivity of sentiment detection. I found that 0.2 is the best, but anything between 0.2-0.5 should work.

## Troubleshooting
### Comments Getting Filtered Incorrectly?
- Adjust the sentiment threshold (higher if too restrictive, lower if too lenient).
- Track debugging logs by using the commented-out print statements.

## Future Improvements
- Expand data sources beyond Reddit (e.g., Twitter, YouTube comments).
- Implement more advanced NLP techniques for topic modeling.
- Visualize trends using interactive sentiment graphs.

## Author
Rachel Ibey

## License
This project is open-source and available under the [MIT License](LICENSE).

