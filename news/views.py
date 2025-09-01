from typing import Dict, Any
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpRequest
from django.conf import settings

from .models import NewsArticle
from .repositories import NewsRepository
from .services.fetchers import RssNewsFetcher, NewsAPIFetcher

class DashboardView(ListView):
    model = NewsArticle
    template_name = "news/dashboard.html"
    context_object_name = "articles"
    paginate_by = 20
    ordering = ["-published_at"]

@require_POST
def fetch_latest(request: HttpRequest):
    repo = NewsRepository()
    items = []

    rss = RssNewsFetcher(settings.NEWS_FEEDS)
    items.extend(rss.fetch())

    api_key = getattr(settings, "NEWSAPI_KEY", "")
    if api_key:
        api = NewsAPIFetcher(api_key=api_key, query="India")
        items.extend(api.fetch())

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

    # Return the latest 20 after fetch
    latest = list(
        NewsArticle.objects.order_by("-published_at")
        .values("title", "summary", "source", "url", "published_at")[:20]
    )

    resp: Dict[str, Any] = {
        "status": "ok",
        "fetched": len(items),
        "created": created,
        "latest": latest,
    }
    return JsonResponse(resp)
