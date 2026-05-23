from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0002_profile_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile",
            old_name="twitter_url",
            new_name="instagram_url",
        ),
    ]
