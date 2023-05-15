from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import F

from .models import *

User = get_user_model()


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'anime']
            )
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('name',)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('name',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('name',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    character = CharacterSerializer()

    class Meta:
        model = Role
        fields = ('character', 'role', 'favorites',)


class AnimeListSerializer(serializers.ModelSerializer):
    user_score = serializers.IntegerField()
    type = TypeSerializer()
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Anime
        fields = ('id', 'title', 'title_english', 'score', 'user_score', 'year', 'type', 'images', 'genres',)


class AnimeRetrieveSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    scored_by = serializers.IntegerField(read_only=True)
    user_score = serializers.IntegerField()
    type = SlugRelatedField(read_only=True, slug_field='name')
    source = SlugRelatedField(read_only=True, slug_field='name')
    rating = SlugRelatedField(read_only=True, slug_field='name')
    genres = GenreSerializer(many=True, read_only=True)
    # HyperlinkedRelatedField сделать с сериализаторе жанра поле юрл на себя(ссылка на вьюху)
    # https://www.django-rest-framework.org/api-guide/relations/
    studios = StudioSerializer(many=True, read_only=True)
    #characters = serializers.SerializerMethodField()

    # def get_characters(self, obj):
    #     characters = obj.characters.all().order_by(F('favorites').desc(nulls_last=True))[:20]
    #     return RoleSerializer(characters, many=True).data

    class Meta:
        model = Anime
        fields = '__all__'
