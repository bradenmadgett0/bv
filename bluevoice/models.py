from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    owner = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_created = models.BooleanField(default = False)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    owner = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, related_name='order', on_delete=models.CASCADE, null=True)