"""
fetch_news.py — pulls live headlines from public RSS feeds and writes stories.json.

No API key required. Run manually:
    python fetch_news.py

Or let app.py call fetch_and_save() automatically on a schedule (see app.py).
"""

import json
import os
import re
import html
import feedparser

DATA_PATH = os.path.join(os.path.dirname(__file__), "stories.json")

# One or more RSS feeds per category. Add/remove feeds here to change sources.
FEEDS = {
    "India": [
        ("Times of India", "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"),
        ("NDTV", "https://feeds.feedburner.com/ndtvnews-top-stories"),
    ],
    "World": [
        ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
        ("Reuters World", "https://www.reutersagency.com/feed/?best-topics=world&post_type=best"),
    ],
    "Tech": [
        ("TechCrunch", "https://techcrunch.com/feed/"),
    ],
    "Business": [
        ("BBC Business", "https://feeds.bbci.co.uk/news/business/rss.xml"),
    ],
    "Politics": [
        ("BBC Politics", "https://feeds.bbci.co.uk/news/politics/rss.xml"),
    ],
}

# How many stories to keep per category per feed
MAX_PER_FEED = 6
# How many top stories (across India + World first) get featured=true in the hero row
FEATURED_COUNT = 5


def clean_summary(raw_summary, max_len=220):
    """Strip HTML tags/entities from RSS summaries and trim to a reasonable length."""
    if not raw_summary:
        return ""
    text = re.sub(r"<[^>]+>", "", raw_summary)
    text = html.unescape(text).strip()
    text = re.sub(r"\s+", " ", text)
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0] + "…"
    return text


def fetch_category(category, feeds):
    """Fetch and normalize entries for a single category from its feed list."""
    items = []
    for source_name, url in feeds:
        try:
            parsed = feedparser.parse(url)
        except Exception as e:
            print(f"[fetch_news] Failed to fetch {source_name} ({url}): {e}")
            continue

        for entry in parsed.entries[:MAX_PER_FEED]:
            title = entry.get("title", "").strip()
            link = entry.get("link", "")
            summary = clean_summary(entry.get("summary", entry.get("description", "")))
            if not title or not link:
                continue
            items.append({
                "category": category,
                "title": title,
                "summary": summary or "Tap through to read the full story.",
                "source": source_name,
                "url": link,
            })
    return items


def fetch_and_save():
    """Fetch all feeds, assign ids/ranks/featured flags, and write stories.json."""
    all_stories = []
    for category, feeds in FEEDS.items():
        all_stories.extend(fetch_category(category, feeds))

    if not all_stories:
        print("[fetch_news] No stories fetched — keeping existing stories.json untouched.")
        return False

    # Rank: India and World stories first (most important), then others,
    # preserving each feed's own top-to-bottom order within that.
    priority = {"India": 0, "World": 1, "Politics": 2, "Business": 3, "Tech": 4}
    all_stories.sort(key=lambda s: priority.get(s["category"], 9))

    for i, story in enumerate(all_stories):
        story["id"] = i + 1
        story["rank"] = i + 1
        story["featured"] = i < FEATURED_COUNT

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(all_stories, f, ensure_ascii=False, indent=2)

    print(f"[fetch_news] Saved {len(all_stories)} stories to {DATA_PATH}")
    return True


if __name__ == "__main__":
    fetch_and_save()
