from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import serializers, status
from rest_framework.response import Response
from . import models 

class MenuItemSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField()
    class Meta:
        model = models.MenuItem
        fields = ['title', 'description', 'price', 'id', 'quantity']

    def get_quantity(self, obj):
        request = self.context['request']
        cart = request.user.cart
        return obj.cartitem_set.filter(cart=cart).first().quantity

    def create(self, validated_data):
         return models.MenuItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['title', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many = True, read_only=True)
    class Meta:
        model = models.Cart
        fields = ['items', 'id', 'owner']

    def create(self, validated_data):
        request = self.context.get('request', None)
        item_id = request.data.get('item')
        
        if item_id == None:
            raise serializers.ValidationError({"message": "Valid menu item is required."})
            
        try:
            item_to_add = models.MenuItem.objects.get(pk=item_id)
        except models.MenuItem.DoesNotExist:
            raise serializers.ValidationError({"message": "Menu item does not exist."})
        try:
            cart = models.Cart.objects.get(owner=request.user)
            try:
                cart_item = models.CartItem.objects.get(cart=cart, item=item_to_add)
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
            except models.CartItem.DoesNotExist:
                cart.items.add(item_to_add)
            cart.save()
            return cart
        except models.Cart.DoesNotExist:
            new_cart = models.Cart.objects.create(owner=request.user)
            item_to_add.count = 1
            new_cart.items.add(item_to_add)
            new_cart.save()
            return new_cart
        
    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        item_id = request.data.get('item')
        quantity = request.data.get('quantity')

        if item_id == None:
            raise serializers.ValidationError({"message": "Valid menu item is required."})
        if quantity == None:
            raise serializers.ValidationError({"message": "Quantity is required."})

        try:
            item_to_update = models.MenuItem.objects.get(pk=item_id)
        except models.MenuItem.DoesNotExist:
            raise serializers.ValidationError({"message": "Menu item does not exist."})
        
        try:
            cart_item = models.CartItem.objects.get(cart=instance, item=item_to_update)
            cart_item.quantity = quantity
            cart_item.save()
        except models.CartItem.DoesNotExist:
            return HttpResponseNotFound()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id', 'cart']