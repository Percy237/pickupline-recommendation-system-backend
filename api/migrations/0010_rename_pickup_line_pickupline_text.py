# Generated by Django 5.0.3 on 2024-04-05 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_pickup_line_id_rating_pickup_line_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pickupline',
            old_name='pickup_line',
            new_name='text',
        ),
    ]
