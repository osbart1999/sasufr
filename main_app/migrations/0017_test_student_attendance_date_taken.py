# Generated by Django 4.2.6 on 2023-11-20 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_test_student_image_image_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_student_attendance',
            name='date_taken',
            field=models.DateField(null=True),
        ),
    ]
