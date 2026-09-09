from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), "stories.json")
CATEGORY_ORDER = ["All", "India", "World", "Tech", "Politics", "Business"]


def load_stories():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
