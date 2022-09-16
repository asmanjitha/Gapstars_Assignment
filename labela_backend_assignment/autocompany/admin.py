from django.contrib import admin
from .models import Cart, Order, Part, User

admin.site.register(Part)
admin.site.register(User)
admin.site.register(Cart)
admin.site.register(Order)

