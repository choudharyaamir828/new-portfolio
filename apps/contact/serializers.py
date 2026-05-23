from rest_framework import serializers

from apps.contact.models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = (
            "id",
            "profile",
            "name",
            "email",
            "recipient_email",
            "subject",
            "message",
            "email_sent",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "profile", "recipient_email", "email_sent")
