from django.db import models
from rest_framework import permissions, viewsets

from user.permissions import IsOwnerOrReadOnly
from .filters import ReviewFilter
from .models import Anime, Character, Review
from .filters import AnimeFilter
from .serializers import (
    AnimeListSerializer,
    CharacterSerializer,
    AnimeRetrieveSerializer,
    ReviewRetrieveSerializer,
    ReviewCreateSerializer,
)


class AnimeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    filterset_class = AnimeFilter

    def get_queryset(self):
        user = self.request.user.id
        queryset = Anime.objects.all().annotate(
            user_score=models.Q(reviews__user=user)
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return AnimeListSerializer
        elif self.action == 'retrieve':
            return AnimeRetrieveSerializer


class CharacterReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (permissions.AllowAny,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    filterset_class = ReviewFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewRetrieveSerializer
        if self.action == 'create':
            return ReviewCreateSerializer
        if self.action in ('retrieve', 'partial_update', 'destroy'):
            return ReviewRetrieveSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('partial_update', 'destroy'):
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
