from django.contrib.auth.models import User

from account.models import Profile


def create_profile(user: User) -> None:
    Profile.objects.get_or_create(user=user)
