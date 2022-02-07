# Generated by Django 4.0.2 on 2022-02-07 13:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordle_app', '0004_alter_game_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='tries',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)]),
        ),
    ]
