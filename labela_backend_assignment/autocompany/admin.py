from django.contrib import admin
from api.models import Cart, Order, Part
from users.models import MyUser as User

admin.site.register(Part)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Order)

