from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

from fetch_news import fetch_and_save

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "stories.json")
CATEGORY_ORDER = ["All", "India", "World", "Tech", "Politics", "Business"]

# Refresh live news every N minutes while the app is running.
REFRESH_MINUTES = 5


def load_stories():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def refresh_news():
    """Pull fresh headlines from RSS feeds. Falls back to existing stories.json on failure."""
    try:
        fetch_and_save()
    except Exception as e:
        print(f"[app] Live news refresh failed, keeping existing stories.json: {e}")


# Fetch live news once when the server starts.
refresh_news()

# Keep refreshing in the background on a timer (works locally and on most hosts;
# on platforms that spin up multiple workers, each worker runs its own timer).
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_news, "interval", minutes=REFRESH_MINUTES)
    scheduler.start()
except Exception as e:
    print(f"[app] Could not start background refresh scheduler: {e}")


@app.route("/")
def index():
    stories = load_stories()
    present = {s["category"] for s in stories}
    categories = [c for c in CATEGORY_ORDER if c == "All" or c in present]
    featured = sorted([s for s in stories if s.get("featured")], key=lambda s: s["rank"])
    return render_template(
        "index.html",
        categories=categories,
        featured=featured,
        today=datetime.now().strftime("%A, %B %d, %Y"),
    )


@app.route("/api/stories")
def api_stories():
    """Returns stories filtered by category and/or top-10 rank."""
    stories = load_stories()

    category = request.args.get("category", "All")
    top10 = request.args.get("top10", "false").lower() == "true"

    if category != "All":
        stories = [s for s in stories if s["category"] == category]

    stories = sorted(stories, key=lambda s: s["rank"])

    if top10:
        stories = stories[:10]

    return jsonify(stories)


@app.route("/api/story/<int:story_id>")
def api_story(story_id):
    stories = load_stories()
    match = next((s for s in stories if s["id"] == story_id), None)
    if not match:
        return jsonify({"error": "not found"}), 404
    return jsonify(match)


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """Manually trigger a live news refresh, e.g. curl -X POST /api/refresh"""
    refresh_news()
    return jsonify({"status": "refreshed", "count": len(load_stories())})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
