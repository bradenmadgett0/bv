from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, generics

from . import serializers
from . import models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class MenuItemsList(generics.ListCreateAPIView): 
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
