# Generated by Django 5.0.6 on 2024-06-29 02:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0003_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='number_of_stars',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='星の数'),
        ),
    ]
