from __future__ import annotations

import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from accounts.forms import (
    ProfileEditForm,
    UserEditForm,
    UserRegistrationForm,
)
from accounts.models import Contact, Profile
from action.models import Action

# Create your views here.


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)  # type: ignore
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related("user", "user__profile")[
        :10
    ]  # One to Many relation
    # actions = actions.prefetch_related("target")[:10] <= Many to Many relation

    return render(
        request,
        "account/dashboard.html",
        {
            "section": "dashboard",
            "actions": actions,
        },
    )


def register(request: HttpRequest) -> HttpResponse:
    user_form = UserRegistrationForm()

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            request.session["pending_registration"] = user_form.cleaned_data
            user_form.send_mail(request)
            messages.success(request, "We have sent an email to your address")
            return redirect("email_validation")
        messages.error(
            request,
            "Error while creating your account, please check your credencials",
        )

    return render(request, "account/register.html", {"user_form": user_form})


def account_activation(
    request: HttpRequest,
    uidb64: str,
    token: str,
) -> HttpResponseRedirect:
    try:
        email = force_str(urlsafe_base64_decode(uidb64))
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
        email = None

    if not email:
        messages.error(request, "Activation link is invalid! (Invalid Email)")
        return redirect("login")

    expected_token = hashlib.sha256(email.encode()).hexdigest()
    if token != expected_token:
        messages.error(request, "Activation link is invalid!")
        return redirect("login")

    pending_registration = request.session.get("pending_registration")
    if not pending_registration or pending_registration["email"] != email:
        messages.error(
            request,
            "Activation link is invalid! (Pending Registration)",
        )
        return redirect("login")

    user = User.objects.create_user(
        username=pending_registration.get("username"),
        email=pending_registration.get("email"),
        first_name=pending_registration.get("first_name"),
        last_name=pending_registration.get("last_name"),
        is_active=True,
    )
    user.set_password(pending_registration.get("password"))
    user.save()
    Profile.objects.create(user=user)
    Action.create_action(user, "Create account")
    login(request, user, settings.AUTHENTICATION_BACKENDS[0])
    messages.success(request, "Account activated successfully!")
    return redirect(reverse("edit"))


@login_required
def edit(
    request: HttpRequest,
) -> HttpResponse | HttpResponseRedirect | HttpResponsePermanentRedirect:
    user_form = UserEditForm(instance=request.user)
    user = User.objects.get(pk=request.user.pk)

    try:
        profile_form = ProfileEditForm(instance=user.profile)  # type: ignore

    # ! In case of user without profile
    except Exception:  # noqa: BLE001
        user_profile = Profile.objects.create(user=user)
        profile_form = (
            ProfileEditForm(instance=user_profile)
            if user_profile
            else ProfileEditForm()
        )

    if request.method == "POST" and user.profile is not None and user:  # type: ignore
        user_form = UserEditForm(instance=user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,  # type: ignore
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            Action.create_action(user, "Edit profile", profile_form.instance)
            messages.success(request, "Profile has been updated successfully")
            return dashboard(request)
        messages.error(request, "Error updating your profile")

    return render(
        request,
        "account/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    users = User.objects.filter(is_active=True)
    return render(
        request,
        "account/user/list.html",
        {
            "section": "people",
            "users": users,
        },
    )


@login_required
def user_detail(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(
        User,
        username=username,
        is_active=True,
    )
    return render(
        request,
        "account/user/detail.html",
        {
            "section": "people",
            "user": user,
        },
    )


@login_required
def user_follow(request: HttpRequest) -> JsonResponse:
    to_user_id = request.POST.get("id")
    action = request.POST.get("action")
    if to_user_id and action:
        try:
            user_from = User.objects.get(pk=request.user.pk)
            user_to = User.objects.get(pk=to_user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=user_from, user_to=user_to)
                Action.create_action(user_from, "Follow", user_to)
            else:
                Contact.objects.filter(user_from=user_from, user_to=user_to).delete()
                Action.create_action(user_from, "Unfollow", user_to)
            return JsonResponse({
                "status": "ok",
                "details": f"Action: {action} to {user_to}",
            })
        except Contact.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "details": "User not found or doesn't exist",
            })
    return JsonResponse({"status": "error", "details": "Invalid request"})


def email_validation(
    request: HttpRequest,
) -> HttpResponse:
    """
    This view is used to inform the user that an email has been sent
    to their address for account activation.
    It is displayed after the user tries to register, between the
    registration and email confirmation steps.
    Waiting until User confirm the email and user can request to send
    the email again if they didn't receive it.
    """
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if not request.session.get("pending_registration"):
            messages.error(
                request,
                "Error while sending the email, please try again later",
            )
            return redirect("register")
        user_form.send_mail(request)
        messages.success(
            request,
            "We have re-sent an email to your address",
        )
        return redirect("email_validation")
    return render(request, "account/email_validation.html")
