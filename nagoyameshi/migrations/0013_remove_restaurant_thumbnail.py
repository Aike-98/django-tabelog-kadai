# Generated by Django 5.0.6 on 2024-07-13 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nagoyameshi', '0012_alter_restaurant_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='thumbnail',
        ),
    ]
