# Generated by Django 3.0.7 on 2021-04-13 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('askcrowd', '0002_auto_20210413_2357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='user1',
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_User', to=settings.AUTH_USER_MODEL),
        ),
    ]
