from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
=======
from django.core.paginator import EmptyPage, Paginator
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
    JsonResponse,
)
>>>>>>> develop
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from account.views import HttpResponsePermanentRedirect, HttpResponseRedirect
from action.utils import create_action
from images.forms import ImageCreateForm
from images.models import Image

# Create your views here.


@login_required
def image_create(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponsePermanentRedirect | HttpResponse:
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            _ = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            # create_action(request.user, "Bookmarked image", new_image)  # type: ignore
            messages.success(request, "Image added successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(
        request,
        "images/image/create.html",
        {
            "section": "images",
            "form": form,
        },
    )


<<<<<<< HEAD
def image_detail(request: HttpRequest, img_id: int, slug: str) -> HttpResponse:
    image = get_object_or_404(Image, pk=img_id, slug=slug)
=======
def image_detail(request: HttpRequest, image_id: int, slug: str) -> HttpResponse:
    image = get_object_or_404(Image, id=image_id, slug=slug)
>>>>>>> develop
    viewed_images = request.session.get("viewed_images", [])

    if image.pk not in viewed_images:
        image.total_views += 1
        image.save()
        viewed_images.append(image.pk)
        request.session["viewed_images"] = viewed_images

    return render(
        request,
        "images/image/detail.html",
        {
            "section": "images",
            "image": image,
            "total_views": image.total_views,
        },
    )


@login_required
@require_POST
def image_like(request: HttpRequest) -> JsonResponse:
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "Like", image)
            else:
                image.users_like.remove(request.user)
                create_action(request.user, "Dislike", image)
            users_like = [
                {
                    "first_name": user.first_name,
                    "profile_photo": (
                        user.profile.photo.url if user.profile.photo else None
                    ),
                }
                for user in image.users_like.all()
            ]
            return JsonResponse({"status": "ok", "users_like": users_like})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, 3)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    try:
<<<<<<< HEAD
        images = paginator.page(page)  # type: ignore
    except PageNotAnInteger:
        images = paginator.page(1)
=======
        images = paginator.page(page or 1)
    # except PageNotAnInteger:
    #     images = paginator.page(1)
>>>>>>> develop
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            "images/image/list_images.html",
            {"section": "images", "images": images},
        )
    return render(
        request,
        "images/image/list.html",
        {"section": "images", "images": images},
    )
