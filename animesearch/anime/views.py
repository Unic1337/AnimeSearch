from django.db import models
from rest_framework import permissions, viewsets, generics
from django_filters import rest_framework
from rest_framework.response import Response
from django.db.models import F, Q, Avg

from user.permissions import IsOwnerOrReadOnly
from .filters import ReviewFilter
from .models import Anime, Review, Character, Role
from .filters import AnimeFilter
from .serializers import (
    AnimeListSerializer,
    RoleSerializer,
    AnimeRetrieveSerializer,
    ReviewSerializer,
    ReviewCreateSerializer, CharacterSerializer,
)


class AnimeReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = AnimeFilter

    def get_queryset(self):
        user = self.request.user.id
        # queryset = Anime.objects.all().annotate(
        #     user_score=models.Case(
        #         models.When(models.Q(reviews__user=user), then=models.F('reviews__score')),
        #         default=None,
        #     )
        # )
        queryset = Anime.objects.annotate(
            user_score=Avg('reviews__score', filter=Q(reviews__user=user))
        )
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            #return AnimeListSerializer
            return AnimeRetrieveSerializer
        elif self.action == 'retrieve':
            return AnimeRetrieveSerializer


class AnimeCharactersAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        anime = kwargs.get('pk')
        instance = Anime.objects.get(pk=anime).characters.all().order_by(F('favorites').desc(nulls_last=True))
        serializer = self.get_serializer(instance, many=True)
        return Response({'data': serializer.data})


class CharacterReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = (permissions.AllowAny,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    filterset_class = ReviewFilter
    # filter_backends = (rest_framework.DjangoFilterBackend,)
    # filterset_fields = ('user', 'anime')

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewSerializer
        if self.action == 'create':
            return ReviewCreateSerializer
        if self.action in ('retrieve', 'partial_update', 'destroy'):
            return ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('partial_update', 'destroy'):
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
