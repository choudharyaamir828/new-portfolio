import logging
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle

from apps.about.models import Profile
from apps.contact.models import ContactMessage
from apps.contact.serializers import ContactMessageSerializer

logger = logging.getLogger(__name__)


def _send_contact_email(message_id, subject, body, recipient_email):
    """Deliver the notification email in a background thread so the
    HTTP request never blocks on (or fails because of) SMTP."""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Contact email delivery failed for message %s", message_id)
        return

    ContactMessage.objects.filter(pk=message_id).update(
        email_sent=True, updated_at=timezone.now()
    )


class ContactMessageCreateView(CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "contact"
    http_method_names = ["post", "options"]

    def perform_create(self, serializer):
        username = self.request.query_params.get("username", "").strip()
        profile = None

        if username:
            profile = Profile.objects.filter(username=username).first()
            if profile is None:
                raise ValidationError({"username": "Profile not found for the given username."})

        recipient_email = (
            (profile.email if profile and profile.email else "")
            or settings.CONTACT_FALLBACK_EMAIL
        )

        if not recipient_email:
            raise ValidationError(
                {"recipient_email": "Recipient email is not configured for this portfolio."}
            )

        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise ValidationError(
                {
                    "email": (
                        "Email delivery is not configured on the server yet. "
                        "Set SMTP credentials in backend environment variables."
                    )
                }
            )

        message = serializer.save(profile=profile, recipient_email=recipient_email)

        subject = f"Portfolio Contact: {message.subject}"
        body = "\n".join(
            [
                f"Portfolio username: {profile.username if profile else 'default'}",
                f"Sender name: {message.name}",
                f"Sender email: {message.email}",
                "",
                "Message:",
                message.message,
            ]
        )

        threading.Thread(
            target=_send_contact_email,
            args=(message.pk, subject, body, recipient_email),
            daemon=True,
        ).start()
