from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

# Create your models here.

class MyUser(AbstractUser):
   name = models.CharField(max_length=250)
   email = models.EmailField(unique=True)
   password = models.CharField(max_length=250)
   username = models.CharField(max_length=250, unique=True)

   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = ['password']

   @classmethod
   def create(cls, name, username, email, password):
      user = cls(name=name, username = username, email=email, password=make_password(password))
      return user

   def __str__(self):
      return "id: " + str(self.id) + ", name: " + self.name
