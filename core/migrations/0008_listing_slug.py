# Generated by Django 4.2.16 on 2024-12-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_listing_default_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='slug',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
