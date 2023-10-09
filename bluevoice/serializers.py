from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import serializers, status
from rest_framework.response import Response
from . import models 

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['title', 'description', 'price', 'id']

    def create(self, validated_data):
         return models.MenuItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    
class CartItemSerializer(serializers.ModelSerializer):
    item = MenuItemSerializer(many=False, read_only=True)
    class Meta:
        model = models.CartItem
        fields = ['cart', 'quantity', 'item', 'id']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = models.Cart
        fields = ['cart_items', 'id', 'owner', 'total']

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
                models.CartItem.objects.create(cart=cart, item=item_to_add, quantity=1)
            cart.total = cart.total + item_to_add.price
            cart.save()
            return cart
        except models.Cart.DoesNotExist:
            new_cart = models.Cart.objects.create(owner=request.user)
            models.CartItem.objects.create(cart=new_cart, item=item_to_add, quantity=1)
            new_cart.total = item_to_add.price
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
            price_diff = (quantity - cart_item.quantity) * item_to_update.price
            cart_item.quantity = quantity
            cart_item.save()
            instance.total += price_diff
            instance.save()
        except models.CartItem.DoesNotExist:
            return HttpResponseNotFound()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'id', 'cart']

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many = False, read_only=True)
    class Meta:
        model = models.Order
        fields = ['owner', 'cart']
    
    def create(self, validated_data):
        request = self.context.get('request', None)
        try:
            current_cart = models.Cart.objects.get(owner=request.user)
        except models.Cart.DoesNotExist:
            return HttpResponseNotFound()
        current_cart.order_created = True
        current_cart.owner = None
        current_cart.save()
        new_order = models.Order.objects.create(owner=request.user, cart=current_cart)
        models.Cart.objects.create(owner=request.user)
        return new_order