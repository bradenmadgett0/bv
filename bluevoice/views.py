from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from rest_framework import viewsets, permissions, serializers as rest_serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


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
            orders = models.Order.objects.filter(owner=request.user.id)
            print(orders)
        except models.Order.DoesNotExist:
            return HttpResponseNotFound()
        serializer = serializers.OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

class BasicAuthLogin(APIView):
    def post(self, request, *args, **kwargs):
        return Response()
    
class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response