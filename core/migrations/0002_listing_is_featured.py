# Generated by Django 4.2.16 on 2024-10-27 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
