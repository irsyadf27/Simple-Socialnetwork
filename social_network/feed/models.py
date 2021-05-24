from django.db import models
from django.utils import timezone


class BaseFeed(models.Model):
    creator = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.id:
            self.created_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        abstract = True


class FeedPost(BaseFeed):
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]


class FeedComment(BaseFeed):
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at"]


class FeedLike(BaseFeed):
    post = models.ForeignKey(FeedPost, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "creator")