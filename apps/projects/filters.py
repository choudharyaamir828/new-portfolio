import django_filters

from apps.projects.models import Project


class ProjectFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="owner__username", lookup_expr="iexact")
    tech_stack = django_filters.CharFilter(method="filter_tech_stack")
    tech_stack__category = django_filters.CharFilter(
        method="filter_tech_stack_category",
    )

    class Meta:
        model = Project
        fields = (
            "username",
            "is_featured",
            "tech_stack",
            "tech_stack__category",
        )

    def filter_tech_stack(self, queryset, name, value):
        return queryset.filter(tech_stack__name__iexact=value).distinct()

    def filter_tech_stack_category(self, queryset, name, value):
        return queryset.filter(tech_stack__category=value).distinct()
