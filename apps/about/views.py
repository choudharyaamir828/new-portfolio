from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound

from apps.about.models import Profile
from apps.about.serializers import ProfileSerializer


class ProfileView(RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self) -> Profile:
        username = self.request.query_params.get("username", "").strip()

        if username:
            try:
                return Profile.objects.get(username=username)
            except Profile.DoesNotExist as exc:
                raise NotFound("Profile not found for the given username.") from exc

        profile = Profile.objects.order_by("created_at").first()
        if profile is None:
            raise NotFound("No portfolio profile found.")
        return profile
