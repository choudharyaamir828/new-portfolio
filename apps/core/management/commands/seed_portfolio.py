from django.core.management.base import BaseCommand

from apps.about.models import Profile
from apps.projects.models import Project, TechStack
from apps.skills.models import Skill, SkillCategory


class Command(BaseCommand):
    help = "Seed sample portfolio data for local development."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding portfolio data..."))

        profile, created = Profile.objects.get_or_create(
            username="aamir",
            defaults={
                "username": "aamir",
                "full_name": "Aamir Khan",
                "title": "Python Backend Developer",
                "bio": (
                    "I build scalable Python backends, REST APIs, admin dashboards, "
                    "and automation systems focused on performance and clean architecture."
                ),
                "email": "aamir@example.com",
                "location": "India",
                "github_url": "https://github.com/aamir-dev",
                "linkedin_url": "https://www.linkedin.com/in/aamir-dev",
                "instagram_url": "",
            },
        )

        if not created:
            profile.username = "aamir"
            profile.full_name = "Aamir Khan"
            profile.title = "Python Backend Developer"
            profile.bio = (
                "I build scalable Python backends, REST APIs, admin dashboards, "
                "and automation systems focused on performance and clean architecture."
            )
            profile.email = "aamir@example.com"
            profile.location = "India"
            profile.github_url = "https://github.com/aamir-dev"
            profile.linkedin_url = "https://www.linkedin.com/in/aamir-dev"
            profile.instagram_url = ""
            profile.save()

        self.stdout.write(self.style.SUCCESS("Profile ready"))

        tech_stack_data = [
            ("Python", "backend"),
            ("Django", "backend"),
            ("Django REST Framework", "backend"),
            ("FastAPI", "backend"),
            ("PostgreSQL", "database"),
            ("SQLite", "database"),
            ("Docker", "devops"),
            ("Redis", "backend"),
            ("Celery", "backend"),
            ("Git", "other"),
        ]

        tech_map = {}
        for name, category in tech_stack_data:
            tech, _ = TechStack.objects.get_or_create(
                name=name,
                defaults={"category": category},
            )
            if tech.category != category:
                tech.category = category
                tech.save(update_fields=["category", "updated_at"])
            tech_map[name] = tech

        self.stdout.write(self.style.SUCCESS("Tech stack ready"))

        skill_category_data = {
            "Backend": [
                ("Python", 95),
                ("Django", 92),
                ("Django REST Framework", 90),
                ("FastAPI", 88),
                ("Celery", 78),
            ],
            "Database": [
                ("PostgreSQL", 85),
                ("SQLite", 82),
                ("Redis", 76),
            ],
            "DevOps": [
                ("Docker", 74),
                ("Git", 86),
            ],
        }

        for order, (category_name, skills) in enumerate(skill_category_data.items(), start=1):
            category, _ = SkillCategory.objects.get_or_create(
                name=category_name,
                profile=profile,
                defaults={"order": order},
            )
            if category.order != order:
                category.order = order
                category.save(update_fields=["order", "updated_at"])

            for skill_name, proficiency in skills:
                skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                category=category,
                defaults={"proficiency": proficiency},
                )
                if skill.proficiency != proficiency:
                    skill.proficiency = proficiency
                    skill.save(update_fields=["proficiency", "updated_at"])

        self.stdout.write(self.style.SUCCESS("Skills ready"))

        project_data = [
            {
                "title": "TaskFlow API",
                "short_description": "A Django REST API for task, team, and role management.",
                "description": (
                    "TaskFlow API is a backend project built with Django REST Framework. "
                    "It includes JWT authentication, role-based permissions, project boards, "
                    "task workflows, and admin reporting."
                ),
                "github_url": "https://github.com/aamir-dev/taskflow-api",
                "live_url": "",
                "is_featured": True,
                "order": 1,
                "stack": ["Python", "Django", "Django REST Framework", "PostgreSQL"],
            },
            {
                "title": "FastAPI Analytics Service",
                "short_description": "A high-performance analytics microservice for dashboards.",
                "description": (
                    "This FastAPI service exposes reporting endpoints, background jobs, "
                    "and aggregated metrics for admin dashboards and product insights."
                ),
                "github_url": "https://github.com/aamir-dev/fastapi-analytics-service",
                "live_url": "",
                "is_featured": True,
                "order": 2,
                "stack": ["Python", "FastAPI", "Redis", "Docker"],
            },
            {
                "title": "Automation Ops Toolkit",
                "short_description": "Python automation scripts for reports, emails, and data sync.",
                "description": (
                    "A collection of automation workflows that process CSV data, schedule jobs, "
                    "sync third-party systems, and reduce repetitive manual operations."
                ),
                "github_url": "https://github.com/aamir-dev/automation-ops-toolkit",
                "live_url": "",
                "is_featured": False,
                "order": 3,
                "stack": ["Python", "SQLite", "Docker", "Git"],
            },
        ]

        for project_item in project_data:
            project, _ = Project.objects.get_or_create(
                title=project_item["title"],
                defaults={
                    "owner": profile,
                    "short_description": project_item["short_description"],
                    "description": project_item["description"],
                    "github_url": project_item["github_url"],
                    "live_url": project_item["live_url"],
                    "is_featured": project_item["is_featured"],
                    "order": project_item["order"],
                },
            )

            project.owner = profile
            project.short_description = project_item["short_description"]
            project.description = project_item["description"]
            project.github_url = project_item["github_url"]
            project.live_url = project_item["live_url"]
            project.is_featured = project_item["is_featured"]
            project.order = project_item["order"]
            project.save()
            project.tech_stack.set([tech_map[name] for name in project_item["stack"]])

        self.stdout.write(self.style.SUCCESS("Projects ready"))
        self.stdout.write(self.style.SUCCESS("Sample portfolio data seeded successfully."))
