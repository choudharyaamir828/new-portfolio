from django.contrib import admin

from apps.skills.models import Skill, SkillCategory


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ("name", "proficiency", "icon")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("profile", "name", "order", "updated_at")
    list_filter = ("profile",)
    list_editable = ("order",)
    search_fields = ("name", "profile__username", "profile__full_name")
    inlines = (SkillInline,)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "icon")
    list_filter = ("category", "category__profile")
    search_fields = ("name",)
