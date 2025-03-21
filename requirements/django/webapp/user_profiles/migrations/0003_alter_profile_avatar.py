# Generated by Django 5.1.4 on 2025-01-07 14:22

import django.core.validators
import user_profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='avatars/default.jpg', upload_to=user_profiles.models.rename_avatar, validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
