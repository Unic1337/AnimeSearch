# Generated by Django 4.1.7 on 2023-05-13 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0004_alter_review_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
