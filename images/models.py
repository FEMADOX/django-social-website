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
    )  # type:ignore
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="images_liked",
        blank=True,
    )  # type:ignore
    title = models.CharField(max_length=200)  # type:ignore
    slug = models.SlugField(max_length=200, blank=True)  # type:ignore
    url = models.URLField(max_length=2000)  # type:ignore
    image = models.ImageField(upload_to="images/%Y/%m/%d")  # type:ignore
    description = models.TextField(blank=True)  # type:ignore
    created_at = models.DateField(auto_now_add=True)  # type:ignore

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "images:detail",
            args=[self.id, self.slug],
        )
