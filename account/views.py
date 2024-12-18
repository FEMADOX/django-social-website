from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from account.forms import ProfileEditForm, UserEditForm, UserRegistrationForm
from account.models import Contact, Profile
from action.models import Action
from action.utils import create_action

# // from account.forms import LoginForm
# // from django.contrib.auth import authenticate, login
# // from django.http import HttpResponse


# Create your views here.


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related("user", "user__profile")[:10]  # One to Many relation
    # actions = actions.prefetch_related("target")[:10] <= Many to Many relation
    
    return render(
        request,
        "account/dashboard.html",
        {
            "section": "dashboard",
            "actions": actions,
        },
    )


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(request.user, "Create account")
            messages.success(request, "Account has been created successfully")
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST" and request.user.profile != None:
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            create_action(request.user, "Edit profile", profile_form)
            messages.success(request, "Profile has been updated successfully")
            return render(request, "account/dashboard.html")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)

        #! In case of user without profile
        try:
            profile_form = ProfileEditForm(instance=request.user.profile)
        except Exception:
            Profile.objects.create(user=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            return redirect(
                request, "account/edit_new_profile.html", {"profile_form": profile_form}
            )

    return render(
        request,
        "account/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        },
    )


@login_required
def user_list(request):
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
def user_detail(request, username: str):
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
@require_POST
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, "Follow", user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
                create_action(request.user, "Unfollow", user)
            return JsonResponse({"status": "ok"})
        except Contact.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})


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
