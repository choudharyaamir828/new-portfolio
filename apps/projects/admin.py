from django.contrib import admin

from apps.projects.models import Project, ProjectImage, TechStack


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption")


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "icon", "updated_at")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "title",
        "slug",
        "is_featured",
        "order",
        "created_at",
    )
    list_filter = ("owner", "is_featured", "tech_stack")
    list_editable = ("is_featured", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "short_description", "owner__username", "owner__full_name")
    filter_horizontal = ("tech_stack",)
    inlines = (ProjectImageInline,)


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "created_at")
    list_filter = ("project",)
    search_fields = ("caption", "project__title")
