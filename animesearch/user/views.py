from django.db import models
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions

from .models import Follow
from .serializers import FollowCreateSerializer, UserRetrieveSerializer, FollowUserIsFollowingSerializer, \
    CurrentUserSerializer

User = get_user_model()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = User.objects.all().annotate(
            followers_number=models.Count('followers')
        ).annotate(
            following_number=models.Count('following')
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        user = kwargs.get('pk')
        action = kwargs.get('action')

        if action in ('following', 'followers'):
            if action == 'following':
                queryset = self.filter_queryset(
                    User.objects.get(pk=user).following.all().values('user_is_following')
                )
            else:
                queryset = self.filter_queryset(
                    User.objects.get(pk=user).followers.all().values('user_is_following')
                )
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = CurrentUserSerializer(page, many=True)
                print(queryset)
                return self.get_paginated_response(serializer.data)
            print(queryset)
            serializer = CurrentUserSerializer(queryset, many=True)
            return Response(serializer.data)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FollowCreateAPIView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
