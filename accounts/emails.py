from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# def send_validation_email(user: User, request: HttpRequest) -> None:
def send_validation_email(
    activation_link: str,
    to_email: str,
) -> None:
    subject = "Activate Your Account"
    html_message = render_to_string(
        "account/email_validation_confirm.html",
        {
            "activation_link": activation_link,
        },
    )

    send_mail(
        subject,
        "",
        settings.EMAIL_HOST_USER,
        [to_email],
        fail_silently=False,
        html_message=html_message,
    )
