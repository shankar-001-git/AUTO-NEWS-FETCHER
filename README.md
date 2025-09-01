# Auto News Fetcher & Dashboard

This is a small Django project I built to practice automating a simple task — fetching latest news headlines and showing them on a frontend dashboard.
The app uses RSS feeds (and optionally NewsAPI) to pull articles, stores them in a SQLite database, and displays them in a clean Bootstrap UI.

# Features

1.Fetches news from multiple RSS feeds (BBC, CNN, Indian Express, etc.)
2.Stores data in SQLite with deduplication (unique URL or title+source)
3.Django model: NewsArticle (title, summary, source, url, published_at)
4.Frontend dashboard (Bootstrap 5) with Fetch Latest News button (AJAX)
5.Management command: python manage.py fetch_news
6.Bonus: background scheduler using django-crontab

# Tech Stack

Python 3.11 + Django 5.x
SQLite (simple setup)
feedparser (RSS parsing)
requests (for NewsAPI)
Bootstrap 5 (UI)
django-crontab (scheduler)

# Setup Instructions

git clone https://github.com/<your-username>/auto-news-fetcher.git
cd auto-news-fetcher
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


# Setup Environment

DEBUG=True
SECRET_KEY=replace_with_any_string
ALLOWED_HOSTS=127.0.0.1,localhost
NEWSAPI_KEY=   # optional


# Run Migrations

python manage.py makemigrations
python manage.py migrate

# Start Server

python manage.py runserver


# UI

Open dashboard
Click Fetch Latest News button
News headlines appear in a list with title, source, and publish date

#Design Decisions

SQLite → kept it simple for testing.
RSS Feeds → no API key required, stable sources
OOP approach → separated fetchers (RssNewsFetcher, NewsAPIFetcher) and DB logic (NewsRepository)
Deduplication → done via url (unique) and (title, source) combo

# Screenshots

ALL THE UI SCREENSHOT IS THERE IN GIT REPO ONLY.

#Author

Made by [SHANKAR KUMAR VISHWAKARMA]
