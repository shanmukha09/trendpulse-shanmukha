import requests
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def categorize(title):
    title = title.lower()
    for category, words in categories.items():
        for word in words:
            if word in title:
                return category
    return None

def fetch(url):
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
    print("Fetching top stories...")

    ids = fetch(TOP_STORIES_URL)
    if not ids:
        print("Failed to fetch IDs")
        return

    #ids = ids[:50]  

    collected = []
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

        if all(v >= 25 for v in count.values()):
            break

    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected, f, indent=4)

    print(f"\nCollected {len(collected)} stories")
    print(f"Saved to {filename}")

if __name__ == "__main__":
    main()