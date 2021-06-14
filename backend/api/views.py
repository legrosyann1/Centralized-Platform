from django.contrib.auth.models import Group, User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import UserProfile
from api.models import UserProfile
from inventory.models import Device, Change
from actions.models import Action, ScheduledTask, LogAction
from .serializers import UserProfileSerializer, GroupSerializer
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.decorators import action
from backend.send_mail import Email
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()



class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def changePassword(self, request, pk=None):
        if request.user.is_superuser and request.user.username != request.data['username']:
            user = User.objects.get(username=request.data['username'])
        else:
            user = request.user

        if not user.is_superuser and user.username != request.data['username']:
            raise PermissionDenied()
        elif not user.check_password(request.data['password']):
            raise AuthenticationFailed()
        else:
            user.set_password(request.data['new_password'])
            user.save()
            return Response("New password was set correctly")


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



class EmailViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        """ Sends email, can contain a file attached to it """
        email = Email()
        isfile = request.data['isfile']
        
        if not isfile:
            file = request.data['files']
            resp = email.send(os.getenv("EMAIL_USER"), 
                              request.data['subject'], 
                              request.data['body'], 
                              file=file, 
                              filename=file.name)
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
        actions = Action.objects.count()
        actionsDone = LogAction.objects.count()
        tasks = ScheduledTask.objects.count()
        tasksEnabled = ScheduledTask.objects.filter(enabled=True)
        deviceChanges = Change.objects.filter(change_code=None)
        devicesHWEndOfLife = Device.objects.filter(hw_end_of_life__lte = datetime.now())
        devicesSWEndOfLife = Device.objects.filter(sw_end_of_life__lte = datetime.now())
        users = UserProfile.objects.count()
        data = {'devices': devices,
                'actions': actions,
                'actionsCompleted': actionsDone,
                'scheduledTasks': tasks, 
                'enabledTasks': len(tasksEnabled),
                'untrackedChanges': len(deviceChanges), 
                'devicesHWEndOfLife': len(devicesHWEndOfLife),
                'devicesSWEndOfLife': len(devicesSWEndOfLife),
                'users': users}
        return Response(data)
