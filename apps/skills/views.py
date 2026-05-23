from rest_framework.generics import ListAPIView

from apps.skills.models import SkillCategory
from apps.skills.serializers import SkillCategorySerializer


class SkillCategoryListView(ListAPIView):
    serializer_class = SkillCategorySerializer
    pagination_class = None

    def get_queryset(self):
        queryset = SkillCategory.objects.select_related("profile").prefetch_related("skills").all()
        username = self.request.query_params.get("username", "").strip()

        if username:
            queryset = queryset.filter(profile__username__iexact=username)

        return queryset
