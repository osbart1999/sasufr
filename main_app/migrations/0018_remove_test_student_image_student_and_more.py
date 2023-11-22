# Generated by Django 4.2.7 on 2023-11-21 18:59

from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0017_test_student_attendance_date_taken"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="test_student_image",
            name="student",
        ),
        migrations.RemoveField(
            model_name="studentfaceimage",
            name="face_image",
        ),
        migrations.AddField(
            model_name="studentfaceimage",
            name="image",
            field=models.ImageField(null=True, upload_to=main_app.models.photo_path),
        ),
        migrations.AddField(
            model_name="studentfaceimage",
            name="image_no",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="studentfaceimage",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student_photos",
                to="main_app.student",
            ),
        ),
        migrations.AlterField(
            model_name="test_student_attendance",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendanciees",
                to="main_app.student",
            ),
        ),
        migrations.DeleteModel(
            name="Test_Student",
        ),
        migrations.DeleteModel(
            name="Test_Student_Image",
        ),
    ]
