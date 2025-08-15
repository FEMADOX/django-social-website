from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django_stubs_ext.db.models.manager import RelatedManager

from accounts.models import Profile
from images.models import Image


class ExtendedProfile(Profile):
    photo: CloudinaryField


class ExtendedUser(User):
    profile: ExtendedProfile
    following: RelatedManager[User]
    followers: RelatedManager[User]

    def get_absolute_url(self) -> None: ...


class ExtendedImage(Image):
    users_like: RelatedManager[ExtendedUser]
