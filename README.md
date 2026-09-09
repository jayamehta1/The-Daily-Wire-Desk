# The Daily Wire Desk

A Flask news site styled like a print newspaper — masthead, ticker, serif type — with a hero section for top India & world stories, category filters, a "Top 10 Today" view, and clickable stories that open full details.

## Demo

![The Daily Wire Desk screenshot](project-demo/demo.png)

## Run locally

```
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000

## Files

- `app.py` — Flask app: page routes + `/api/stories` (filter by `category`/`top10`) + `/api/story/<id>` (single story for the modal)
- `stories.json` — the news data. Edit this to add/update stories. Fields: `category`, `title`, `summary`, `source`, `url`, `rank`, `featured` (true = shows in hero)
- `templates/index.html` — page template
- `static/style.css`, `static/app.js` — styling and frontend logic (filtering, ticker, modal)
- `project-demo/screenshot.png` — screenshot used above

## Push to GitHub

```
git init
git add .
git commit -m "Daily Wire Desk"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

## Deploy (GitHub Pages won't work — it's static-only, this needs Python)

- **Render.com**: New → Web Service → connect repo → build `pip install -r requirements.txt` → start `gunicorn app:app`
- **Railway.app**: New Project → Deploy from GitHub → auto-detects Flask
- **PythonAnywhere**: upload repo, point WSGI file to `app.py`

All auto-deploy on every `git push`.