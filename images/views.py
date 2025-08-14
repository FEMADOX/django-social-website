from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render

from action.models import Action
from images.forms import ImageCreateForm
from images.models import Image

# Create your views here.


@login_required
def image_create(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    user = User.objects.get(pk=request.user.pk)

    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            Action.create_action(user, "Bookmarked image", new_image)
            messages.success(request, "Image added successfully")
            return redirect(new_image.get_absolute_url())
        messages.error(request, "The formulary wasn't valid, please submit valid data")
    else:
        form = ImageCreateForm(data=request.GET)

    return render(
        request,
        "images/create.html",
        {
            "section": "images",
            "form": form,
        },
    )


def image_detail(request: HttpRequest, img_id: int, slug: str) -> HttpResponse:
    image = get_object_or_404(Image, pk=img_id, slug=slug)
    viewed_images = request.session.get("viewed_images", [])

    if image.pk not in viewed_images:
        image.total_views += 1
        image.save()
        viewed_images.append(image.pk)
        request.session["viewed_images"] = viewed_images

    return render(
        request,
        "images/detail.html",
        {
            "section": "images",
            "image": image,
            "total_views": image.total_views,
        },
    )


@login_required
def image_like(request: HttpRequest) -> JsonResponse:
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    user = User.objects.get(pk=request.user.pk)

    if not image_id or not action:
        return JsonResponse({
            "status": "error",
            "details": "Image ID and Action required",
        })

    try:
        image = Image.objects.get(id=image_id)
        if action == "like":
            image.users_like.add(user)
            Action.create_action(user, "Like", image)
        else:
            image.users_like.remove(user)
            Action.create_action(user, "Dislike", image)
        users_like = [
            {
                "first_name": user.first_name,
                "profile_photo": (
                    user.profile.photo.url if user.profile.photo else None  # type: ignore
                ),
                "profile_url": user.get_absolute_url(),  # type: ignore
            }
            for user in image.users_like.select_related("profile").all()
        ]
        return JsonResponse({"status": "ok", "users_like": users_like})
    except Image.DoesNotExist:
        return JsonResponse({"status": "error", "details": "Image doesn't exist"})


@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    try:
        images = paginator.page(page or 1)
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            "images/list_images.html",
            {"section": "images", "images": images},
        )
    return render(
        request,
        "images/list.html",
        {"section": "images", "images": images},
    )
