from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .models import MyUser as User
from autocompany.serializers import  UserSerializer

# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['user_id'] = user.id

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#--------------------------------USER-------------------------------------------------------------------
@api_view(['GET'])
def user_list(request):
    
    if request.method == 'GET':
        #get all the users
        #serialize and return as a JSON
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def user_signup(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    name = request.data['name']
    user = User.create(name=name, username=username, email=email, password=password)
    serializer = UserSerializer(data=user.__dict__)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg':'user created, please login now', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response({'error': 'user creation failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']
    user = User.create(username=username, email=email, password=password)
    serializer = UserSerializer(data=user.__dict__)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg':'user created, please login now', 'data':serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': 'user creation failed'}, status=status.HTTP_400_BAD_REQUEST)