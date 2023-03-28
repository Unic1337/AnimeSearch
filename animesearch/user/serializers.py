from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from anime.serializers import ReviewRetrieveSerializer
from .models import Follow

User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'image_url', 'last_login',
            'date_joined', 'is_active', 'is_superuser', 'is_staff',
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    reviews = ReviewRetrieveSerializer(many=True)
    followers_number = serializers.IntegerField()
    following_number = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'image_url', 'last_login', 'date_joined',
            'followers_number', 'following_number', 'reviews',
        )


class FollowCreateSerializer(serializers.ModelSerializer):
    user_is_following = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user_is_following', 'user_is_being_followed']
            )
        ]

    # def create(self, validated_data):
    #     print(self, validated_data)


class FollowRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class FollowUserIsFollowingSerializer(serializers.ModelSerializer):
    user_is_following = UserRetrieveSerializer(many=True)

    class Meta:
        model = Follow
        fields = ['user_is_following']
