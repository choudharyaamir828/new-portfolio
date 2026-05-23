from rest_framework import serializers

from apps.skills.models import Skill, SkillCategory


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            "id",
            "name",
            "proficiency",
            "icon",
        )
        read_only_fields = fields


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    profile_username = serializers.CharField(source="profile.username", read_only=True)

    class Meta:
        model = SkillCategory
        fields = (
            "id",
            "profile_username",
            "name",
            "order",
            "skills",
        )
        read_only_fields = fields
