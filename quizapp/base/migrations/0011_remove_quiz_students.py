# Generated by Django 4.2.4 on 2023-08-10 13:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0010_quiz_students"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quiz",
            name="students",
        ),
    ]