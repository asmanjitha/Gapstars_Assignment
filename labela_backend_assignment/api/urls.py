from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('parts', views.part_list, name='parts'),
    path('parts/<int:id>', views.part_details, name='part_details'),
    path('cart', views.user_cart, name='user_cart'),
    path('orders', views.order, name='orders'),
    path('orders/update', views.update_order, name='update'),
    path('purchase', views.purchase, name='purchase'),
    # path('users/token', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('users/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]