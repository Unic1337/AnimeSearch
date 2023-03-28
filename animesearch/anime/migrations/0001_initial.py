# Generated by Django 4.1.7 on 2023-03-12 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('images', models.JSONField()),
                ('trailer', models.JSONField()),
                ('title', models.TextField()),
                ('title_english', models.TextField(null=True)),
                ('title_japanese', models.TextField(null=True)),
                ('type', models.TextField()),
                ('source', models.TextField()),
                ('episodes', models.IntegerField(null=True)),
                ('status', models.TextField()),
                ('airing', models.BooleanField()),
                ('aired', models.TextField()),
                ('duration', models.TextField()),
                ('rating', models.TextField()),
                ('score', models.FloatField(null=True)),
                ('scored_by', models.IntegerField(null=True)),
                ('favorites', models.IntegerField()),
                ('synopsis', models.TextField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('studios', models.JSONField()),
                ('genres', models.JSONField()),
            ],
            options={
                'verbose_name': ('anime',),
                'verbose_name_plural': ('anime',),
                'db_table': 'anime',
                'managed': False,
            },
        ),
    ]
