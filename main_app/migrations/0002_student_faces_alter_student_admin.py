# Generated by Django 4.2.4 on 2023-10-30 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='faces',
            field=models.ImageField(blank=True, null=True, upload_to='faces/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='admin',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
