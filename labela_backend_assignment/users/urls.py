from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('signup', views.user_signup, name='user_signup'),
    path('users_list', views.user_list, name='user_list'),
    path('login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh', TokenRefreshView.as_view(), name='token_refresh'),
]