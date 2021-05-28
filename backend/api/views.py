from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import UserProfile
from inventory.models import Device
from .serializers import UserProfileSerializer, GroupSerializer
from backend.send_mail import Email
from dotenv import load_dotenv
import os

load_dotenv()



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



class EmailViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """Sends email, can contain files attached to it"""
        email = Email()
        isfile = request.data['isfile']
        
        if not isfile:
            file = request.data['files']
            resp = email.send(os.getenv("EMAIL_USER"), request.data['subject'], request.data['body'], file=file, filename=file.name)
        else:
            resp = email.send(os.getenv("EMAIL_USER"), request.data['subject'], request.data['body'])

        if resp == '1':
            return Response('200')
        else:
            return Response('500')


class MetricsViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        devices = Device.objects.count()
        data = {'devices': devices}
        return Response(data)
