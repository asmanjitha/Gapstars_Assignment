from django.db import models
from django.core.validators import int_list_validator, validate_comma_separated_integer_list
from django.contrib.auth.models import AbstractUser


# class MyUser(AbstractUser):
#    name = models.CharField(max_length=250)
#    email = models.EmailField(unique=True)
#    password = models.CharField(max_length=250)
#    username = models.CharField(max_length=250, unique=True)

#    @classmethod
#    def create(cls, name, username, email, password):
#       user = cls(name=name, username = username, email=email, password=make_password(password))
#       return user

#    def __str__(self):
#       return "id: " + str(self.id) + ", name: " + self.name

# class Part(models.Model):
#      name = models.CharField(max_length=250)
#      description = models.CharField(max_length=1000)
#      price = models.FloatField(null=True)

#      def __str__(self):
#         return "id: " + str(self.id) + ", name: " + self.name

# class Cart(models.Model):
#    user_id = models.IntegerField()
#    parts = models.CharField(max_length=1000, validators=[int_list_validator])

#    @classmethod
#    def create(cls, user_id):
#       cart = cls(user_id=user_id)
#       return cart


# class Order(models.Model):
#    user_id = models.IntegerField()
#    parts = models.CharField(max_length = 1000, validators=[int_list_validator])
#    delivery_time = models.DateTimeField(null=True, blank=True)

#    @classmethod
#    def create(cls, user_id, parts):
#       order = cls(user_id=user_id, parts=parts)
#       return order
