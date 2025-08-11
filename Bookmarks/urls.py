from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("account/", include("accounts.urls")),
    path("images/", include("images.urls", namespace="images")),
    path("accounts/", include("allauth.urls")),
    re_path(
        r".*\.js\.map$",
        lambda: HttpResponse(status=204),
    ),  # Disable sourcemaps
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
