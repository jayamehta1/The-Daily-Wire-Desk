<div align="center">

# 📰 The Daily Wire Desk

**A print-style daily news web app — clickable stories, and a Top 10 Today view.**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

[Features](#-features) • [Demo](#-demo) • [Quick Start](#-quick-start) • [Project Structure](#-project-structure) • [Customize](#-customize-the-news) • [Deploy](#-deploy)

</div>

---

## ✨ Features

- 🗞️ **Print-newspaper design** — masthead, scrolling ticker, serif type
- 🇮🇳 **Hero section** — top India & world stories featured up front
- 🖱️ **Clickable stories** — click any card to open the full story in a modal, with a link to the original source
- 🏷️ **Category filters** — India, World, Tech, Politics, Business
- ⭐ **Top 10 Today** — ranks and numbers the day's biggest stories
- 🔌 **Simple data layer** — all news lives in one editable `stories.json`, no database needed

---

## 📸 Demo

<details open>
<summary><b>🏠 Home page — masthead, ticker, hero stories</b></summary>
<br>

![Home page](project-demo/home.png)

</details>

<details>
<summary><b>🗂️ Category filter in action</b></summary>
<br>

![Category filter](project-demo/filter.png)

</details>

<details>
<summary><b>⭐ Top 10 Today view</b></summary>
<br>

![Top 10 Today](project-demo/top10.png)

</details>

<details>
<summary><b>📖 Story modal — click any card to read more</b></summary>
<br>

![Story modal](project-demo/modal.png)

</details>

<details>
<summary><b>📱 Mobile view</b></summary>
<br>

![Mobile view](project-demo/mobile.png)

</details>

> Drop your own screenshots into `project-demo/` using the filenames above and they'll show up here automatically on GitHub.

---

## 🚀 Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd daily-wire-desk
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** 🎉

---

## 🗂️ Project Structure

```
daily-wire-desk/
├── app.py                  # Flask routes + API
├── stories.json            # 📝 all news content lives here
├── templates/
│   └── index.html          # page template
├── static/
│   ├── style.css           # newspaper theme
│   └── app.js               # filtering, ticker, modal logic
├── project-demo/           # screenshots for this README
├── requirements.txt
├── Procfile
└── README.md
```

---

## ✍️ Customize the News

All content lives in `stories.json` — no code changes needed to update headlines:

```json
{
  "id": 1,
  "category": "India",
  "title": "Your headline here",
  "summary": "Two or three sentence summary.",
  "source": "Source Name",
  "url": "https://source-website.com/article",
  "rank": 1,
  "featured": true
}
```

| Field | What it does |
|---|---|
| `category` | Controls filter chip + color tag (`India`, `World`, `Tech`, `Politics`, `Business`) |
| `rank` | Lower number = higher priority in "Top 10 Today" and the ticker |
| `featured` | `true` puts it in the hero row up top |
| `url` | Where "Read full story →" links to |

---

## ☁️ Deploy

> ⚠️ **GitHub Pages won't work** — it only serves static files, and this app needs Python running.

<details>
<summary><b>Render.com</b> (recommended, free tier)</summary>
<br>

1. New → Web Service → connect this repo
2. Build command: `pip install -r requirements.txt`
3. Start command: `gunicorn app:app`

</details>

<details>
<summary><b>Railway.app</b></summary>
<br>

1. New Project → Deploy from GitHub
2. Auto-detects Flask, no config needed

</details>

<details>
<summary><b>PythonAnywhere</b></summary>
<br>

1. Upload the repo
2. Point the WSGI config file to `app.py`

</details>

All three auto-redeploy on every `git push`.

---

<div align="center">

Made with ☕ and Flask

</div>
