from django.conf import settings
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import AllowAny

from apps.about.models import Profile
from apps.contact.models import ContactMessage
from apps.contact.serializers import ContactMessageSerializer


class ContactMessageCreateView(CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
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

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
            )
        except Exception as exc:
            raise APIException("Message saved, but email delivery failed.") from exc

        message.email_sent = True
        message.save(update_fields=["email_sent", "updated_at"])
