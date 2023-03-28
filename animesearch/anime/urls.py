from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import *


urlpatterns = format_suffix_patterns([
    path('anime/', AnimeReadOnlyViewSet.as_view({'get': 'list'})),
    path('anime/<int:pk>/', AnimeReadOnlyViewSet.as_view({'get': 'retrieve'})),
    path('characters/', CharacterReadOnlyViewSet.as_view({'get': 'list'})),
    path('characters/<int:pk>/', CharacterReadOnlyViewSet.as_view({'get': 'retrieve'})),
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('reviews/<int:pk>/', ReviewViewSet.as_view(
        {'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'}
    )),
])
