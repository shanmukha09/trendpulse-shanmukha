"""
Task 1: Data Collection Script

This script collects top stories from Hacker News (news.ycombinator.com),
categorizes them into predefined categories based on keywords in the titles,
and saves the collected data to a JSON file. It aims to gather up to 25 stories
per category for trend analysis.

Author: [Your Name]
Date: [Current Date]
"""

import requests
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

# URL to fetch the list of top story IDs from Hacker News API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"

# Dictionary defining categories and their associated keywords for story classification
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def categorize(title):
    """
    Categorizes a story title based on predefined keywords.

    Args:
        title (str): The title of the story to categorize.

    Returns:
        str or None: The category name if a keyword matches, otherwise None.
    """
    title = title.lower()
    for category, words in categories.items():
        for word in words:
            if word in title:
                return category
    return None

def fetch(url):
    """
    Fetches JSON data from a given URL with error handling.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict or None: The JSON response if successful, otherwise None.
    """
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            return r.json()
        else:
            print("Failed request:", url)
    except Exception as e:
        print("Error:", e)
    return None

def main():
    """
    Main function to collect and categorize top stories from Hacker News.

    Fetches top story IDs, retrieves story details, categorizes them,
    collects up to 25 stories per category, and saves the data to a JSON file.
    """
    print("Fetching top stories...")

    ids = fetch(TOP_STORIES_URL)
    if not ids:
        print("Failed to fetch IDs")
        return

    # Uncomment the next line to limit to first 50 stories for testing
    #ids = ids[:50]  

    collected = []
    # Initialize count dictionary to track stories per category
    count = {c: 0 for c in categories}

    print("Processing stories...")

    for i in ids:
        print("Checking story:", i)

        story = fetch(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")

        if not story or "title" not in story:
            continue

        cat = categorize(story["title"])
        if not cat:
            continue

        # Skip if already have 25 stories for this category
        if count[cat] >= 25:
            continue

        collected.append({
            "post_id": i,
            "title": story["title"],
            "category": cat,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        count[cat] += 1

        # Stop if all categories have reached 25 stories
        if all(v >= 25 for v in count.values()):
            break

    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Generate filename with current date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=4)

    print(f"\nCollected {len(collected)} stories")
    print(f"Saved to {filename}")

if __name__ == "__main__":
    # Run the main function when the script is executed directly
    main()
