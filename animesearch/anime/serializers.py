from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from .models import Anime, Character, Review

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


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class AnimeListSerializer(serializers.ModelSerializer):
    user_score = serializers.IntegerField()

    class Meta:
        model = Anime
        fields = ('id', 'title', 'title_english', 'title_japanese',
                  'score', 'scored_by', 'user_score', 'year', 'type', 'images',)


class AnimeRetrieveSerializer(serializers.ModelSerializer):
    reviews = ReviewRetrieveSerializer(many=True)

    class Meta:
        model = Anime
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
