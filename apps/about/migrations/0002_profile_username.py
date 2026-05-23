from django.db import migrations, models
from django.utils.text import slugify


def populate_profile_usernames(apps, schema_editor):
    Profile = apps.get_model("about", "Profile")

    for profile in Profile.objects.order_by("id"):
        if profile.username:
            continue

        base_slug = slugify(profile.full_name) or f"profile-{profile.id}"
        candidate = base_slug
        counter = 2

        while Profile.objects.exclude(pk=profile.pk).filter(username=candidate).exists():
            candidate = f"{base_slug}-{counter}"
            counter += 1

        profile.username = candidate
        profile.save(update_fields=["username"])


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="username",
            field=models.SlugField(blank=True, max_length=60, null=True),
        ),
        migrations.RunPython(populate_profile_usernames, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="profile",
            name="username",
            field=models.SlugField(max_length=60, unique=True),
        ),
    ]
