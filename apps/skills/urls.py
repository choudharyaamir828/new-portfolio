from django.urls import path

from apps.skills.views import SkillCategoryListView


urlpatterns = [
    path("", SkillCategoryListView.as_view(), name="skills-list"),
]
