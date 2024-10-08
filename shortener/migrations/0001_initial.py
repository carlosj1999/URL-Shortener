# Generated by Django 5.0.6 on 2024-09-06 02:24

import shortener.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShortenedURL",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("original_url", models.URLField(max_length=500)),
                (
                    "short_code",
                    models.CharField(
                        default=shortener.models.generate_short_code,
                        max_length=6,
                        unique=True,
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
