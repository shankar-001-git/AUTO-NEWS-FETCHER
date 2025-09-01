from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    source = models.CharField(max_length=255)
    url = models.URLField(unique=True)  # primary dedupe
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["published_at"]),
            models.Index(fields=["source"]),
        ]
        constraints = [
            # Secondary dedupe (helps when some feeds omit stable URLs)
            models.UniqueConstraint(
                fields=["title", "source"],
                name="uniq_title_source"
            )
        ]

    def __str__(self) -> str:
        return f"{self.source} | {self.title[:80]}"


