# Generated by Django 5.1.6 on 2025-02-17 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configapp', '0002_actor_movie_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_user',
            field=models.BooleanField(default=False),
        ),
    ]
