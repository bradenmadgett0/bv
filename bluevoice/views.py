from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import viewsets, permissions, serializers as rest_serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from . import serializers
from . import models

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            cart = models.Cart.objects.get(owner=request.user.id)
        except models.Cart.DoesNotExist:
            return HttpResponseNotFound()
        serializer = serializers.CartSerializer(cart, many=False)
        return Response(serializer.data)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            order = models.Order.objects.get(owner=request.user.id)
        except models.Order.DoesNotExist:
            return HttpResponseNotFound()
        serializer = serializers.OrderSerializer(order, many=False)
        return Response(serializer.data)
    