# Generated by Django 5.0.3 on 2024-04-21 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_rename_pickup_line_rating_pickup_line_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='pickup_line_id',
            new_name='pickup_line',
        ),
    ]