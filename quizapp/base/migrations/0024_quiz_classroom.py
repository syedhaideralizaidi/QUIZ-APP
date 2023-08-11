# Generated by Django 4.2.4 on 2023-08-11 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0023_remove_classroom_quizzes_delete_classroomquizhistory"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="classroom",
            field=models.ForeignKey(
                default=3,
                on_delete=django.db.models.deletion.CASCADE,
                to="base.classroom",
            ),
        ),
    ]