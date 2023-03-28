from django.urls import path
from user.views import *


urlpatterns = [
    path('auth/users/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_retrieve'),
    path('auth/users/<int:pk>/<str:action>/', UserRetrieveAPIView.as_view(), name='user_following'),
    path('auth/users/<int:pk>/followers/', UserRetrieveAPIView.as_view(), name='user_followers'),
    path('follow/', FollowCreateAPIView.as_view(), name='follow_create'),
]
