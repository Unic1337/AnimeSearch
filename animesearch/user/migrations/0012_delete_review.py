# Generated by Django 4.1.7 on 2023-03-26 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_review_anime_alter_review_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]