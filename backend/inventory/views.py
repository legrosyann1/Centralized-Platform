from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .models import Device
from .serializers import DevicesSerializer


class DevicesViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = Device.objects.all()
    serializer_class = DevicesSerializer
    permission_classes = [permissions.IsAuthenticated]