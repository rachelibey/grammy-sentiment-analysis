
import praw
from secret import id, secret, agent
import json
import os
import time

# Reddit API credentials
reddit = praw.Reddit(
    client_id=id,
    client_secret=secret,
    user_agent=agent
)

queries = {
    "popheads": ["Kendrick Lamar Grammy", "Taylor Swift Grammy", "Beyonce Grammy", "Billie Eilish Grammy",
                 "The Beatles Grammy", "Sabrina Carpenter Grammy", "Charli XCX Grammy", "Chappell Roan Grammy",
                 "Andre 3000 Grammy", "Jacob Collier Grammy", "Shaboozey Grammy", "Lady Gaga Grammy",
                 "Bruno Mars Grammy", "Benson Boone Grammy", "Doechii Grammy", "Kruangbin Grammy", "Raye Grammy",
                 "Teddy Swims Grammy"],
    "music": ["Grammy", "Best New Artist", "Billie Eilish", "Record of the Year", "ROTY", "The Beatles",
              "Beyonce", "Sabrina Carpenter", "Charli XCX", "Kendrick Lamar", "Chappell Roan", "Taylor Swift",
              "Album of the Year", "AOTY", "Andre 3000", "Jacob Collier", "Song of the Year", "Shaboozey",
              "Lady Gaga", "Bruno Mars", "Benson Boone", "Doechii", "Khruangbin", "Raye", "Teddy Swims"],
    "popculturechat": ["Grammy", "Grammys"]
}

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Moves up from src/
output_dir = os.path.join(base_dir, "data/reddit_data")
os.makedirs(output_dir, exist_ok=True)

current_year = 2025
start_of_year = int(time.mktime(time.strptime(f"{current_year}-01-01", "%Y-%m-%d")))

def scrape_reddit_comments(subreddit_name, query_list):
    output_file = os.path.join(output_dir, f"{subreddit_name}.json")

    # Load existing data if file exists
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            subreddit_comments = json.load(f)

    else:
        subreddit_comments = {}

    for query in query_list:
        print(f"Searching r/{subreddit_name} for '{query}'...")

        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.search(query, sort="new", limit=10)  # Newest posts

        for post in posts:
            post.comments.replace_more(limit=0)
            filtered_comments = [c.body for c in post.comments.list() if c.created_utc >= start_of_year]

            if query not in subreddit_comments:
                subreddit_comments[query] = []

            subreddit_comments[query].extend(filtered_comments)

    # Save updated data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(subreddit_comments, f, indent=4)

    print(f"Updated {output_file} with new comments.\n")


for subreddit, query_list in queries.items():
    scrape_reddit_comments(subreddit, query_list)

print("Completed!")
