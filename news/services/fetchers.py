from __future__ import annotations
from dataclasses import dataclass
from typing import List, Iterable, Optional
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser
import requests

@dataclass
class NewsItem:
    title: str
    summary: str
    source: str
    url: str
    published_at: datetime

class BaseNewsFetcher:
    def fetch(self) -> List[NewsItem]:
        raise NotImplementedError

    @staticmethod
    def _safe_dt(value: Optional[str]) -> datetime:
        """
        Parse RFC2822/HTTP dates safely; fallback to UTC now.
        """
        if not value:
            return datetime.now(tz=timezone.utc)
        try:
            dt = parsedate_to_datetime(value)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return datetime.now(tz=timezone.utc)

class RssNewsFetcher(BaseNewsFetcher):
    """
    Fetches from one or more RSS/Atom feeds using feedparser.
    """

    def __init__(self, feeds: Iterable[str], source_label: Optional[str] = None) -> None:
        self.feeds = list(feeds)
        self.source_label = source_label  # optional: override source name

    def fetch(self) -> List[NewsItem]:
        items: List[NewsItem] = []
        for feed_url in self.feeds:
            parsed = feedparser.parse(feed_url)
            # derive a reasonable source label
            if isinstance(parsed.feed, dict):
                src = self.source_label or parsed.feed.get("title", "RSS")
            else:
                src = self.source_label or "RSS"
            for e in parsed.entries:
                raw_title = e.get("title", "")
                if isinstance(raw_title, list):
                    title = " ".join(str(t) for t in raw_title).strip()
                elif isinstance(raw_title, str):
                    title = raw_title.strip()
                else:
                    title = str(raw_title).strip()
                if not title:
                    continue
                link = e.get("link") or e.get("id") or ""
                # Ensure link is a string
                if isinstance(link, list):
                    link = " ".join(str(l) for l in link).strip()
                else:
                    link = str(link).strip()
                if not link:
                    continue
                raw_summary = e.get("summary") or e.get("description") or ""
                if isinstance(raw_summary, list):
                    summary = " ".join(str(s) for s in raw_summary).strip()
                else:
                    summary = str(raw_summary).strip()
                # prefer 'published', fallback to 'updated'
                published = e.get("published") or e.get("updated")
                # Ensure published is a string or None
                if isinstance(published, list):
                    published_str = " ".join(str(p) for p in published).strip()
                elif isinstance(published, str) or published is None:
                    published_str = published
                else:
                    published_str = str(published).strip()
                dt = self._safe_dt(published_str)

                items.append(
                    NewsItem(
                        title=title,
                        summary=summary,
                        source=src,
                        url=link,
                        published_at=dt,
                    )
                )
        return items

class NewsAPIFetcher(BaseNewsFetcher):
    """
    Optional fetcher using newsapi.org (needs API key).
    """

    def __init__(self, api_key: str, query: str = "top headlines", language: str = "en") -> None:
        self.api_key = api_key
        self.query = query
        self.language = language

    def fetch(self) -> List[NewsItem]:
        url = "https://newsapi.org/v2/top-headlines"
        params = {"q": self.query, "language": self.language, "pageSize": 50}
        headers = {"X-Api-Key": self.api_key}
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()
        items: List[NewsItem] = []
        for a in data.get("articles", []):
            title = (a.get("title") or "").strip()
            link = a.get("url") or ""
            if not title or not link:
                continue
            summary = (a.get("description") or a.get("content") or "").strip()
            source = (a.get("source", {}) or {}).get("name") or "NewsAPI"
            published = a.get("publishedAt")  # ISO8601
            try:
                dt = datetime.fromisoformat(published.replace("Z", "+00:00")) if published else datetime.now(tz=timezone.utc)
            except Exception:
                dt = datetime.now(tz=timezone.utc)

            items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    source=source,
                    url=link,
                    published_at=dt,
                )
            )
        return items



