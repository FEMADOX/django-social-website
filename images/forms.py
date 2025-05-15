import cloudinary
import cloudinary.uploader
from django import forms
from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,
        }

    def clean_url(self) -> str:
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            error_message = "The given URL does not match valid image extensions."
            raise forms.ValidationError(error_message)
        return url

    def save(self, commit: bool = True) -> Image:
        image: Image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        image_title = (
            self.cleaned_data["title"]
            if len(self.cleaned_data["title"]) < 50  # noqa: PLR2004
            else self.cleaned_data["title"][:50] + "..."
        )
        image_description = self.cleaned_data["description"]
        name = slugify(image.title)
        # extension = image_url.rsplit(".", 1)[1].lower()
        # image_name = f"{name}.{extension}"
        upload_result = cloudinary.uploader.upload(
            image_url,
            folder="Social_Website/media/images/",
        )
        image.title = image_title
        image.slug = name
        image.description = image_description
        image.image = upload_result["secure_url"]

        if commit:
            image.save()
        return image
