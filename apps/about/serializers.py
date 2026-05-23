from rest_framework import serializers

from apps.about.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "username",
            "full_name",
            "title",
            "bio",
            "profile_image",
            "resume",
            "email",
            "location",
            "github_url",
            "linkedin_url",
            "instagram_url",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
