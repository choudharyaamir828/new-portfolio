from django.db import models

from apps.core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    profile = models.ForeignKey(
        "about.Profile",
        related_name="contact_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    recipient_email = models.EmailField(blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"
