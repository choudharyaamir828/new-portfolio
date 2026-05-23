from django.contrib import admin

from apps.contact.models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "recipient_email",
        "profile",
        "subject",
        "email_sent",
        "is_read",
        "created_at",
    )
    list_filter = ("email_sent", "is_read", "created_at", "profile")
    search_fields = ("name", "email", "recipient_email", "subject", "message")
    actions = ("mark_as_read",)

    def get_readonly_fields(self, request, obj=None):
        return tuple(field.name for field in self.model._meta.fields)

    def has_add_permission(self, request) -> bool:
        return False

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset) -> None:
        queryset.update(is_read=True)
