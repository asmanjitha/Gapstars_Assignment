from django.db import models
from django.core.validators import int_list_validator


class Part(models.Model):
     name = models.CharField(max_length=250)
     description = models.CharField(max_length=1000)
     price = models.FloatField(null=True)

     def __str__(self):
        return "id: " + str(self.id) + ", name: " + self.name

class Cart(models.Model):
   user_id = models.IntegerField()
   parts = models.CharField(max_length=1000, validators=[int_list_validator])

   @classmethod
   def create(cls, user_id):
      cart = cls(user_id=user_id)
      return cart


class Order(models.Model):
   user_id = models.IntegerField()
   parts = models.CharField(max_length = 1000, validators=[int_list_validator])
   delivery_time = models.DateTimeField(null=True, blank=True)

   @classmethod
   def create(cls, user_id, parts):
      order = cls(user_id=user_id, parts=parts)
      return order