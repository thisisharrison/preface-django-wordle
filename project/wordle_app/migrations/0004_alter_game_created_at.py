# Generated by Django 4.0.2 on 2022-02-06 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wordle_app', '0003_remove_game_created_date_game_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
