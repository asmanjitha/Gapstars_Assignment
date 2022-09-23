from django.test import TestCase, Client
from django.urls import reverse
from api.models import Cart, Order, Part
from users.models import MyUser as User
import json
from rest_framework_simplejwt.tokens import RefreshToken
from autocompany.serializers import  UserSerializer
from users.views import TokenObtainPairSerializer

class TestModels(TestCase):
    def setUp(self):
        self.user1 = User.create(
            name='user',
            email='email@email.com',
            username='email@email.com',
            password='password'
        )

        self.cart1 = Cart.create(
            user_id=1
        )

        self.order1 = Order.create(
            user_id=1,
            parts='1'
        )
    
    def test_user_create_method(self):
        self.assertIsNotNone(self.user1)

    def test_user_pw_hashing(self):
        self.assertNotEquals('password', self.user1.password)
    
    def test_cart_create_method(self):
        self.assertIsNotNone(self.cart1)
    
    def test_order_create_method(self):
        self.assertIsNotNone(self.cart1)
