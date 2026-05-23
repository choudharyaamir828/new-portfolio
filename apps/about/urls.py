from django.urls import path

from apps.about.views import ProfileView


urlpatterns = [
    path("", ProfileView.as_view(), name="about"),
]
