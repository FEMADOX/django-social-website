from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from account.forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from account.models import Contact, Profile
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
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            Action.create_action(new_user, "Create account")
            messages.success(request, "Account has been created successfully")
            return render(request, "account/register_done.html", {"new_user": new_user})
        messages.error(request, "Error while creating your account, please try again")
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


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
        profile_form = ProfileEditForm(instance=user_profile)
        return redirect(
            "account/edit_new_profile.html",
            {"profile_form": profile_form},
        )

    if request.method == "POST" and user.profile is not None:  # type: ignore
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
# @require_POST
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


# // def user_login(request):

# //     if request.method == "POST":
# //         form = LoginForm(request.POST)
# //         if form.is_valid():
# //             cd = form.cleaned_data
# //             user = authenticate(
# //                 request,
# //                 username=cd["username"],
# //                 password=cd["password"],
# //             )
# //             if user is not None:
# //                 if user.is_active:
# //                     login(request, user)
# //                     return HttpResponse("Authenticated succesfully")
# //                 else:
# //                     return HttpResponse("Disabled Account")
# //             else:
# //                 return HttpResponse("Invalid Login")
# //     else:
# //         form = LoginForm()
# //     return render(request, "account/login.html", {"form": form})
