# Generated by Django 4.1.6 on 2023-05-23 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "url",
                    models.CharField(
                        blank=True, max_length=255, unique=True, verbose_name="Url"
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="child",
                        to="main_body.menu",
                    ),
                ),
            ],
            options={
                "verbose_name": "Menu",
                "verbose_name_plural": "Menu",
                "ordering": ("pk",),
            },
        ),
        migrations.CreateModel(
            name="PageVisits",
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
                ("url", models.CharField(default=None, max_length=255, unique=True)),
                ("count", models.PositiveIntegerField(default=0)),
                ("session_id", models.CharField(db_index=True, max_length=150)),
            ],
            options={
                "verbose_name_plural": "Page Visits",
            },
        ),
        migrations.CreateModel(
            name="Weather",
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
                ("ip", models.CharField(default="unavailable", max_length=50)),
                ("address", models.CharField(default="unavailable", max_length=250)),
                ("temp", models.IntegerField(default=0)),
                ("feels_like", models.IntegerField(default=0)),
                ("humidity", models.IntegerField(default=0)),
                ("wind", models.IntegerField(default=0)),
                ("clouds", models.CharField(default="unavailable", max_length=25)),
            ],
            options={
                "verbose_name_plural": "weather",
            },
        ),
        migrations.CreateModel(
            name="MenuRelation",
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
                (
                    "from_parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relations_with_child",
                        to="main_body.menu",
                    ),
                ),
                (
                    "to_child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="relations_with_parent",
                        to="main_body.menu",
                    ),
                ),
            ],
            options={
                "verbose_name": "MenuRelation",
                "verbose_name_plural": "MenuRelations",
            },
        ),
    ]
