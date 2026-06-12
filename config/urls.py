from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.static import serve

from apps.core.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("health/", HealthCheckView.as_view(), name="health"),
                path("about/", include("apps.about.urls")),
                path("projects/", include("apps.projects.urls")),
                path("skills/", include("apps.skills.urls")),
                path("contact/", include("apps.contact.urls")),
            ],
        ),
    ),
]

urlpatterns += [
    path(
        "media/<path:path>",
        serve,
        {"document_root": settings.MEDIA_ROOT},
        name="media",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
