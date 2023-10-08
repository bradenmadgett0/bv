from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    owner = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(MenuItem, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)