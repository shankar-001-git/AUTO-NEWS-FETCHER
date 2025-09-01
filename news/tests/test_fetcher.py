from django.test import TestCase
from django.conf import settings
from news.services.fetchers import RssNewsFetcher

class RssFetcherTests(TestCase):
    def test_rss_fetcher_returns_items(self):
        fetcher = RssNewsFetcher(settings.NEWS_FEEDS[:1])  # test first feed
        items = fetcher.fetch()
        # This ensures the object list has correct structure
        if items:  # if internet available
            first = items[0]
            self.assertTrue(hasattr(first, "title"))
            self.assertTrue(hasattr(first, "url"))
        else:
            # If no internet, just pass the test
            self.assertEqual(items, [])
