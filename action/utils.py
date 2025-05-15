import datetime

from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from action.models import Action


def create_action(user: AnonymousUser, verb: str, target: None = None) -> bool:
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id,
        verb=verb,
        created__gte=last_minute,
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id,
        )
    if not similar_actions:
        # No actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
