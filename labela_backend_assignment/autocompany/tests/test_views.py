from http import client
from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from api.models import Cart, Order, Part
from users.models import MyUser as User
import json
from rest_framework_simplejwt.tokens import RefreshToken
from autocompany.serializers import  UserSerializer, CartSerializer
from users.views import MyTokenObtainPairSerializer, TokenObtainPairSerializer

class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.create(
            username="testUser@gmail.com",
            name="testuser",
            email="testUser@gmail.com",
            password="testPassword"
        )
        serializer = UserSerializer(data=cls.user.__dict__)
        if serializer.is_valid():
            serializer.save()
    
    def test_user_save_db(self):
        self.assertTrue(User.objects.filter(email = self.user.email).exists())

    def test_user_signup(self):
        client = Client()
        data = {
            "username":"asm",
            "email":"email@email.com",
            "password":"pass",
            "name":"name"
        }
        response = client.post(reverse('user_signup'), data=data)
        self.assertEquals(response.status_code, 201)
    
    def test_users_list(self):
        client = Client()
        response = client.get(reverse('user_list'))

        self.assertEquals(response.status_code, 200)
    
    def test_parts_list_GET_Unauthorized(self):
        client = Client()
        response = client.get(reverse('parts'))

        self.assertEquals(response.status_code, 401)
    
    def test_parts_list_GET(self):
        dbUser = User.objects.get(email = self.user.email)
        self.token = str(MyTokenObtainPairSerializer.get_token(user=dbUser).access_token)
        client = Client()     
        header = {'HTTP_AUTHORIZATION':'Bearer ' + self.token}

        response = client.get(reverse('parts'), **header)

        self.assertEquals(response.status_code, 200)
    
    def test_part_save(self):
        dbUser = User.objects.get(email = self.user.email)
        self.token = str(MyTokenObtainPairSerializer.get_token(user=dbUser).access_token)
        client = Client()   
        header = {'HTTP_AUTHORIZATION':'Bearer ' + self.token}
        data = {'name':'test part', 'price':10, 'description':'test part description'}

        response = client.post(reverse('parts'),data=data,  **header)

        self.assertEquals(response.status_code, 201)
    
    def test_GET_user_cart_empty(self):
        dbUser = User.objects.get(email = self.user.email)
        self.token = str(MyTokenObtainPairSerializer.get_token(user=dbUser).access_token)
        client = Client()   
        header = {'HTTP_AUTHORIZATION':'Bearer ' + self.token}

        response = client.get(reverse('user_cart'), **header)

        self.assertEquals(response.status_code, 404)
    
    def test_GET_user_cart_non_empty(self):
        dbUser = User.objects.get(email = self.user.email)
        self.token = str(MyTokenObtainPairSerializer.get_token(user=dbUser).access_token)
        client = Client()   
        header = {'HTTP_AUTHORIZATION':'Bearer ' + self.token}

        cart = Cart.create(user_id=dbUser.id)
        parts = []
        parts.append(str(1))

        cart.parts = ",".join(parts)
        serializer = CartSerializer(cart, data = cart.__dict__)
        if serializer.is_valid():
            serializer.save()

        response = client.get(reverse('user_cart'), **header)

        self.assertEquals(response.status_code, 200)
    
    def test_purchase(self):
        dbUser = User.objects.get(email = self.user.email)
        self.token = str(MyTokenObtainPairSerializer.get_token(user=dbUser).access_token)
        client = Client()   
        header = {'HTTP_AUTHORIZATION':'Bearer ' + self.token}

        cart = Cart.create(user_id=dbUser.id)
        parts = []
        parts.append(str(1))

        cart.parts = ",".join(parts)
        serializer = CartSerializer(cart, data = cart.__dict__)
        if serializer.is_valid():
            serializer.save()
        

        response = client.post(reverse('purchase'), **header)
        self.assertEquals(response.status_code, 202)
        self.assertTrue(Order.objects.filter(user_id = dbUser.id).exists())



