# Generated by Django 4.1.7 on 2023-03-12 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='date joined',
            new_name='date_joined',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='email address',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user image',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='active',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='staff',
            new_name='is_staff',
        ),
    ]
