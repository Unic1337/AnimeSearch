# Generated by Django 4.1.7 on 2023-03-12 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_date joined_user_date_joined_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='verified',
            new_name='is_verified',
        ),
    ]
