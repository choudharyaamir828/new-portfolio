from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("about/", include("apps.about.urls")),
                path("projects/", include("apps.projects.urls")),
                path("skills/", include("apps.skills.urls")),
                path("contact/", include("apps.contact.urls")),
            ],
        ),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
