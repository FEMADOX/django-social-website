from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts import views
from accounts.forms import CustomPasswordResetForm

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path("users/", views.user_list, name="user_list"),
    path("users/follow/", views.user_follow, name="user_follow"),
    path("users/<username>", views.user_detail, name="user_detail"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm),
        name="password_reset",
    ),
    path(
        "activation/<uidb64>/<token>/",
        views.account_activation,
        name="account_activation",
    ),
    path("email-validation/", views.email_validation, name="email_validation"),
]
