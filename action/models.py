from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(
        "auth.User",
        related_name="actions",
        on_delete=models.CASCADE,
    )  # type:ignore
    verb = models.CharField(max_length=255)  # type:ignore
    created = models.DateTimeField(auto_now_add=True)  # type:ignore
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )  # type: ignore
    target_id = models.PositiveIntegerField(blank=True, null=True)  # type: ignore
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
