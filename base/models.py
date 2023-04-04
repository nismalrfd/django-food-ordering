from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your models here.

class PizzaCategory(models.Model):
    category_name = models.CharField(max_length=100)


class Pizza(models.Model):
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE, related_name='category')
    pizza_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(upload_to='pizza')


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Pizza,on_delete=models.CASCADE,related_name='coupons')
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.code


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='carts')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    instamojo_id = models.CharField(max_length=1000)

    def get_cart_total(self):
        return CartItems.objects.filter(cart=self).aggregate(Sum('pizza__price'))['pizza__price__sum']


class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
