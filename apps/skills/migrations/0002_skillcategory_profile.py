import django.db.models.deletion
from django.db import migrations, models


def populate_skillcategory_profiles(apps, schema_editor):
    Profile = apps.get_model("about", "Profile")
    SkillCategory = apps.get_model("skills", "SkillCategory")

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
            twitter_url="",
        )

    SkillCategory.objects.filter(profile__isnull=True).update(profile=profile)


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0002_profile_username"),
        ("skills", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="skillcategory",
            name="profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skill_categories",
                to="about.profile",
            ),
        ),
        migrations.AlterField(
            model_name="skillcategory",
            name="name",
            field=models.CharField(max_length=60),
        ),
        migrations.RunPython(populate_skillcategory_profiles, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="skillcategory",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skill_categories",
                to="about.profile",
            ),
        ),
        migrations.AddConstraint(
            model_name="skillcategory",
            constraint=models.UniqueConstraint(
                fields=("profile", "name"),
                name="unique_skill_category_per_profile",
            ),
        ),
    ]
