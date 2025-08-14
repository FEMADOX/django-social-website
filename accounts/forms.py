import hashlib
import logging
from typing import Any

from allauth.utils import build_absolute_uri
from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode

from .models import Profile

# Code Down Here


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        max_length=50,
        required=True,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Repeat password",
        max_length=50,
        required=True,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        widgets = {
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }

    def clean_password_2(self) -> str:
        cleaned_data = self.cleaned_data
        if cleaned_data["password"] != cleaned_data["password2"]:
            error_message = "Passwords don't match"
            raise forms.ValidationError(error_message)
        return cleaned_data["password2"]

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists."
            raise forms.ValidationError(error_message)
        return email

    def send_mail(  # noqa: PLR0913, PLR0917
        self,
        request: HttpRequest,
    ) -> None:
        email = request.session["pending_registration"]["email"]
        subject = "Account Activation"
        message = ""
        activation_link = build_absolute_uri(
            request,
            reverse(
                "account_activation",
                kwargs={
                    "uidb64": urlsafe_base64_encode(email.encode()),
                    "token": hashlib.sha256(email.encode()).hexdigest(),
                },
            ),
        )
        html_email_template_name = render_to_string(
            "account/email_validation_confirm.html",
            {
                "activation_link": activation_link,
            },
        )
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=html_email_template_name,
            )
        except Exception as error:
            logger = logging.getLogger(__name__)
            logger.exception(f"SMTP error occurred while sending email {error}")  # noqa: G004, TRY401


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            },
        ),
    )

    def send_mail(  # noqa: PLR0913, PLR0917
        self,
        subject_template_name: str,
        email_template_name: str,
        context: dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = None,
    ) -> None:
        subject = "Password Reset Email"
        message = ""
        html_email_template_name = render_to_string(
            "registration/password_reset_email.html",
            context,
        )
        to_email = self.cleaned_data["email"]
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email],
                fail_silently=False,
                html_message=html_email_template_name,
            )
        except Exception as error:
            logger = logging.getLogger(__name__)
            logger.exception(f"SMTP error occurred while sending email {error}")  # noqa: G004, TRY401
