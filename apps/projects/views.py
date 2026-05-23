from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from apps.projects.filters import ProjectFilter
from apps.projects.models import Project
from apps.projects.serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
)


class ProjectListView(ListAPIView):
    serializer_class = ProjectListSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = ProjectFilter
    search_fields = ["title", "short_description"]
    ordering_fields = ["order", "created_at"]

    def get_queryset(self):
        return Project.objects.select_related("owner").prefetch_related("tech_stack").all()


class ProjectDetailView(RetrieveAPIView):
    serializer_class = ProjectDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Project.objects.select_related("owner").prefetch_related("tech_stack", "gallery").all()
        username = self.request.query_params.get("username", "").strip()

        if username:
            queryset = queryset.filter(owner__username__iexact=username)

        return queryset
