from django.contrib import admin

from apps.about.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "title", "email", "updated_at")
    search_fields = ("username", "full_name", "email")
    readonly_fields = ("created_at", "updated_at")
