from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="images_created",
        on_delete=models.CASCADE,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, auto_created=True)
    url = models.URLField(max_length=2000, blank=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    total_likes = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["-total_likes"]),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse(
            "images:detail",
            args=[self.pk, self.slug],
        )
