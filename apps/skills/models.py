from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel


class SkillCategory(TimeStampedModel):
    profile = models.ForeignKey(
        "about.Profile",
        related_name="skill_categories",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=60)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "skill categories"
        constraints = [
            models.UniqueConstraint(
                fields=("profile", "name"),
                name="unique_skill_category_per_profile",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.profile.username} / {self.name}"


class Skill(TimeStampedModel):
    name = models.CharField(max_length=80)
    category = models.ForeignKey(
        SkillCategory,
        related_name="skills",
        on_delete=models.CASCADE,
    )
    proficiency = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    icon = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-proficiency", "name"]

    def __str__(self) -> str:
        return self.name
