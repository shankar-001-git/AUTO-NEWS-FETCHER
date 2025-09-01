from django.core.management.base import BaseCommand
from django.conf import settings

from news.repositories import NewsRepository
from news.services.fetchers import RssNewsFetcher, NewsAPIFetcher

class Command(BaseCommand):
    help = "Fetch latest news into the database (RSS by default, NewsAPI if configured)."

    def handle(self, *args, **options):
        repo = NewsRepository()
        items = []

        # Prefer RSS (no API key needed)
        rss = RssNewsFetcher(settings.NEWS_FEEDS)
        items.extend(rss.fetch())

        # Optionally add NewsAPI results if key is present
        api_key = getattr(settings, "NEWSAPI_KEY", "")
        if api_key:
            api = NewsAPIFetcher(api_key=api_key, query="India")
            items.extend(api.fetch())

        # Convert NewsItem -> dicts for repository
        payload = [
            {
                "title": i.title,
                "summary": i.summary,
                "source": i.source,
                "url": i.url,
                "published_at": i.published_at,
            }
            for i in items
        ]

        created = repo.bulk_save_unique(payload)
        self.stdout.write(self.style.SUCCESS(f"Fetched {len(items)}, created {created} new articles."))



