# Generated by Django 4.2.7 on 2023-11-22 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0019_remove_test_student_attendance_attendance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="studentfaceimage",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="student_photos",
                to="main_app.student",
            ),
        ),
        migrations.DeleteModel(
            name="UploadedFile",
        ),
    ]
