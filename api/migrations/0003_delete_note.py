# Generated by Django 5.0.3 on 2024-04-01 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_category_userprofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Note',
        ),
    ]
