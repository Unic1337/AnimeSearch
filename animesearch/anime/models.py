from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Type(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'anime_type'


class Source(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'anime_source'


class Rating(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'anime_rating'


class Genre(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'anime_genre'


class Studio(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'anime_studio'


class Character(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)
    images = models.JSONField()

    class Meta:
        managed = False
        db_table = 'anime_character'
        verbose_name = 'Character'
        verbose_name_plural = 'Characters'
        ordering = ['pk']


class Role(models.Model):
    ROLE_CHOICES = [
        ('MAIN', 'Main'),
        ('SUPP', 'Supporting'),
    ]
    id = models.IntegerField(primary_key=True, null=False)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    favorites = models.IntegerField(null=True)
    role = models.CharField(
        max_length=4,
        choices=ROLE_CHOICES,
        default='MAIN',
    )

    class Meta:
        managed = False
        db_table = 'anime_role'


class Anime(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    images = models.JSONField()
    trailer = models.JSONField()
    title = models.CharField(max_length=100)
    title_english = models.CharField(null=True, max_length=100)
    title_japanese = models.CharField(null=True, max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    episodes = models.IntegerField(null=True)
    status = models.CharField(max_length=100)
    airing = models.BooleanField()
    aired = models.JSONField()
    duration = models.CharField(max_length=100)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    score = models.FloatField(null=True)
    scored_by = models.IntegerField(null=True)
    favorites = models.IntegerField()
    synopsis = models.TextField(null=True)
    season = models.TextField(null=True)
    year = models.PositiveSmallIntegerField(null=True)
    genres = models.ManyToManyField(Genre, related_name='genres', symmetrical=False)
    studios = models.ManyToManyField(Studio, related_name='studios', symmetrical=False)
    characters = models.ManyToManyField(Role, related_name='characters', symmetrical=False)

    class Meta:
        managed = False
        db_table = 'anime_anime'
        verbose_name = 'Anime'
        verbose_name_plural = 'Anime'
        ordering = ['pk']


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, related_name='reviews', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'anime_review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk']
