from rest_framework import serializers

from apps.projects.models import Project, ProjectImage, TechStack


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = (
            "id",
            "name",
            "icon",
            "category",
        )
        read_only_fields = fields


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = (
            "id",
            "image",
            "caption",
        )
        read_only_fields = fields


class ProjectListSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "owner_username",
            "title",
            "slug",
            "short_description",
            "featured_image",
            "tech_stack",
            "is_featured",
        )
        read_only_fields = fields


class ProjectDetailSerializer(serializers.ModelSerializer):
    tech_stack = TechStackSerializer(many=True, read_only=True)
    gallery = ProjectImageSerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "owner_username",
            "title",
            "slug",
            "short_description",
            "description",
            "featured_image",
            "live_url",
            "github_url",
            "tech_stack",
            "is_featured",
            "order",
            "gallery",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields
