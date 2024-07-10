# Generated by Django 5.0.6 on 2024-07-02 06:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_email_verified_at_alter_customuser_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(110)], verbose_name='age'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='customer_id',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='customer id'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(regex='^[0-9]{10,11}$')], verbose_name='phone number'),
        ),
    ]
