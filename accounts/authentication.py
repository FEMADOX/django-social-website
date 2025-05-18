# from django.contrib.auth.models import User

# from accounts.models import Profile


# def create_profile(
#     details: dict[str, str],
#     *args: tuple[None],  # noqa: ARG001
#     **kwargs: dict,  # noqa: ARG001
# ) -> None:  # noqa: ARG001
#     user, _ = User.objects.get_or_create(
#         username=details.get("username"),
#         email=details.get("email"),
#         first_name=details.get("first_name"),
#         last_name=details.get("last_name"),
#     )
#     Profile.objects.get_or_create(user=user)
