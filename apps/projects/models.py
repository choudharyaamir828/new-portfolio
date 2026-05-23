from django.db import models
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class TechStack(TimeStampedModel):
    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DATABASE = "database", "Database"
        DEVOPS = "devops", "DevOps"
        OTHER = "other", "Other"

    name = models.CharField(max_length=60, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=40, choices=Category.choices)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Project(TimeStampedModel):
    owner = models.ForeignKey(
        "about.Profile",
        related_name="projects",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    featured_image = models.ImageField(upload_to="projects/", blank=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    tech_stack = models.ManyToManyField(
        TechStack,
        related_name="projects",
        blank=True,
    )
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self) -> str:
        return f"{self.owner.username} / {self.title}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            candidate = base_slug
            counter = 2
            while Project.objects.exclude(pk=self.pk).filter(
                slug=candidate,
            ).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        related_name="gallery",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return self.caption or f"Image for {self.project.title}"
