from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    photo = CloudinaryField(
        "image",
        blank=True,
        folder="Social_Website/media/users/",
        default="https://res.cloudinary.com/dd1qoripz/image/upload/v1745813449/No_Image_Available_wvog0c.jpg",
        transformation={
            "width": 500,
            "height": 500,
            "crop": "fill",
            "quality": "auto",
            "fetch_format": "auto",
        },
    )

    def __str__(self) -> str:
        return f"Profile of {self.user.username}"


class Contact(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name="rel_from_set",
        on_delete=models.CASCADE,
    )
    user_to = models.ForeignKey(
        User,
        related_name="rel_to_set",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"{self.user_from} follows {self.user_to}"


user_model = get_user_model()
user_model.add_to_class(
    "following",
    models.ManyToManyField(
        "self",
        through=Contact,
        related_name="followers",
        symmetrical=False,
    ),
)
