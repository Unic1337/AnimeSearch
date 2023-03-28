from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Anime(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    images = models.JSONField()
    trailer = models.JSONField()
    title = models.CharField(max_length=100)
    title_english = models.CharField(null=True, max_length=100)
    title_japanese = models.CharField(null=True, max_length=100)
    type = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    episodes = models.IntegerField(null=True)
    status = models.CharField(max_length=100)
    airing = models.BooleanField()
    aired = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    score = models.FloatField(null=True)
    scored_by = models.IntegerField(null=True)
    favorites = models.IntegerField()
    synopsis = models.TextField(null=True)
    year = models.PositiveSmallIntegerField(null=True)
    studios = models.JSONField()
    genres = models.JSONField()

    class Meta:
        managed = False
        db_table = 'anime'
        verbose_name = 'Anime'
        verbose_name_plural = 'Anime'
        ordering = ['pk']


class Character(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    favorites = models.IntegerField()
    images = models.JSONField()
    anime = models.ForeignKey(Anime, related_name='characters', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'character'
        verbose_name = 'Character'
        verbose_name_plural = 'Characters'
        ordering = ['pk']


class Review(models.Model):
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, related_name='reviews', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    date_added = models.DateTimeField(name='date_added', auto_now_add=True)
    title = models.CharField(name='title', max_length=100, blank=True, null=True)
    body = models.TextField(name='body', blank=True, null=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk']
