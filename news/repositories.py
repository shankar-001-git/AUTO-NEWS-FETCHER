from typing import Iterable, List
from django.utils import timezone
from .models import NewsArticle

class NewsRepository:
    """
    Encapsulates DB operations for NewsArticle (OOP-friendly).
    """

    def bulk_save_unique(self, items: Iterable[dict]) -> int:
        """
        items: iterable of dicts with keys: title, summary, source, url, published_at
        Uses bulk_create(ignore_conflicts=True) for URL uniqueness,
        and also benefits from unique (title, source) constraint.
        Returns count of actually created rows.
        """
        candidates: List[NewsArticle] = []
        now = timezone.now()

        for it in items:
            candidates.append(
                NewsArticle(
                    title=it["title"][:500],
                    summary=it.get("summary", "") or "",
                    source=it["source"][:255],
                    url=it["url"],
                    published_at=it.get("published_at") or now,
                )
            )

        created = NewsArticle.objects.bulk_create(
            candidates, ignore_conflicts=True
        )
        return len(created)
