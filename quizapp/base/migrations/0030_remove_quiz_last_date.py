# Generated by Django 4.2.4 on 2023-08-11 16:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0029_alter_quiz_last_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quiz",
            name="last_date",
        ),
    ]