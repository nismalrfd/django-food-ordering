from django.contrib import admin
from base.models import *
# Register your models here.

admin.site.register(PizzaCategory)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Coupon)