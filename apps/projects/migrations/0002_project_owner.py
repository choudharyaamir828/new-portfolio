import django.db.models.deletion
from django.db import migrations, models


def populate_project_owners(apps, schema_editor):
    Profile = apps.get_model("about", "Profile")
    Project = apps.get_model("projects", "Project")

    profile = Profile.objects.order_by("id").first()
    if profile is None:
        profile = Profile.objects.create(
            username="default",
            full_name="Default Profile",
            title="",
            bio="",
            email="default@example.com",
            location="",
            github_url="",
            linkedin_url="",
        )

    Project.objects.filter(owner__isnull=True).update(owner=profile)


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0002_profile_username"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="about.profile",
            ),
        ),
        migrations.RunPython(populate_project_owners, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="project",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="projects",
                to="about.profile",
            ),
        ),
    ]
