# Generated by Django 4.2.4 on 2023-08-10 18:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0015_quiz_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quiz",
            name="students",
            field=models.ManyToManyField(
                limit_choices_to={"is_student": True},
                related_name="assigned_quizzes",
                through="base.QuizAssignment",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]