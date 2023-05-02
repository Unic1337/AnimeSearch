from django.db import models
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions

from anime.models import Anime
from anime.serializers import AnimeListSerializer
from .models import Follow
from .serializers import (
    FollowCreateSerializer,
    UserRetrieveSerializer,
    FollowUserIsFollowingSerializer,
    FollowUserIsBeingFollowedSerializer,
)

User = get_user_model()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = User.objects.all().annotate(
            following_number=models.Count('following', distinct=True)
        ).annotate(
            followers_number=models.Count('followers', distinct=True)
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = kwargs.get('pk')
        action = kwargs.get('action')

        if action in ('following', 'followers', 'reviews',):
            if action == 'following':
                queryset = self.filter_queryset(
                    User.objects.get(pk=user).following.all()
                )
                serializer_class = FollowUserIsBeingFollowedSerializer

            if action == 'followers':
                queryset = self.filter_queryset(
                    User.objects.get(pk=user).followers.all()
                )
                serializer_class = FollowUserIsFollowingSerializer

            if action == 'reviews':
                queryset = Anime.objects.all().filter(
                    models.Q(reviews__user=user)).annotate(
                    user_score=models.F('reviews__score')
                )
                serializer_class = AnimeListSerializer

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FollowCreateAPIView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
