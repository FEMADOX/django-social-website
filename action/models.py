from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class Action(models.Model):
    user: models.ForeignKey = models.ForeignKey(
        User,
        related_name="actions",
        on_delete=models.CASCADE,
    )
    verb: models.CharField = models.CharField(max_length=255)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    target_ct: models.ForeignKey = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id: models.PositiveIntegerField = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
