# Generated by Django 4.0.2 on 2022-02-19 13:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wordle_app', '0007_alter_game_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
