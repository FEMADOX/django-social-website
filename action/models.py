import datetime

from django.contrib.auth.models import AbstractUser, User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(
        User,
        related_name="actions",
        on_delete=models.CASCADE,
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    target = GenericForeignKey("target_ct", "target_id")

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Action by {self.user} - {self.verb} on {self.created}"

    @staticmethod
    def create_action(
        user: User | AbstractUser,
        verb: str,
        target: models.Model | None = None,
    ) -> bool:
        now = timezone.now()
        last_minute = now - datetime.timedelta(seconds=60)
        similar_actions = Action.objects.filter(
            user_id=user.pk,
            verb=verb,
            created__gte=last_minute,
        )
        # Don't save admins users actions
        if user.is_staff or user.is_superuser:
            return False
        if target:
            target_ct = ContentType.objects.get_for_model(target)
            similar_actions = similar_actions.filter(
                target_ct=target_ct,
                target_id=target.pk,
            )
        if not similar_actions:
            # No actions found
            action = Action(user=user, verb=verb, target=target)
            action.save()
            return True
        return False
