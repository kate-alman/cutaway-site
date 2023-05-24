# Generated by Django 4.1.6 on 2023-05-24 09:41

from django.db import migrations


def set_menu(apps, schema_editor):
    Menu = apps.get_model("main_body", "menu")

    Menu.objects.create(name="Home")
    services = Menu.objects.create(name="Services", url="services")
    Menu.objects.create(name="Blog", url="blog", parent=services)
    Menu.objects.create(name="Film", url="film", parent=services)
    Menu.objects.create(name="Documentation", url="schema-swagger-ui", parent=services)
    about = Menu.objects.create(name="About", url="about")
    Menu.objects.create(name="Feedback", url="feedback", parent=about)


class Migration(migrations.Migration):
    dependencies = [
        ("main_body", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(set_menu),
    ]
