from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class Profile(TimeStampedModel):
    username = models.SlugField(max_length=60, unique=True)
    full_name = models.CharField(max_length=120)
    title = models.CharField(max_length=150)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="profile/", blank=True)
    resume = models.FileField(upload_to="resume/", blank=True)
    email = models.EmailField()
    location = models.CharField(max_length=120, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    def __str__(self) -> str:
        return self.username or self.full_name or "Portfolio Profile"

    def save(self, *args, **kwargs) -> None:
        if not self.username:
            base_slug = slugify(self.full_name) or "profile"
            candidate = base_slug
            counter = 2
            while Profile.objects.exclude(pk=self.pk).filter(username=candidate).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.username = candidate

        super().save(*args, **kwargs)
