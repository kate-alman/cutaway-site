# Generated by Django 4.1.6 on 2023-05-23 14:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FavoriteRelationship",
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
            ],
        ),
        migrations.CreateModel(
            name="Profile",
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
                ("nickname", models.CharField(blank=True, max_length=50, unique=True)),
                ("bio", models.TextField(blank=True, max_length=500)),
                ("location", models.CharField(blank=True, max_length=50)),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="/user_photos/non_photo.png",
                        upload_to="user_photos/%Y/%m/%d/",
                    ),
                ),
                (
                    "favorites",
                    models.ManyToManyField(
                        related_name="favorite_relationship",
                        through="accounts.FavoriteRelationship",
                        to="accounts.profile",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="favoriterelationship",
            name="from_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="from_people",
                to="accounts.profile",
            ),
        ),
        migrations.AddField(
            model_name="favoriterelationship",
            name="to_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="to_people",
                to="accounts.profile",
            ),
        ),
    ]
