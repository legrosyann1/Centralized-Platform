from rest_framework import viewsets, generics, permissions
from actions.models import LogAction, Action, ScheduledTask
from actions.serializers import LogActionSerializer, ActionSerializer, ScheduledTaskSerializer
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import mixins

# Create your views here.

class ActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class LogActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = LogAction.objects.all().order_by('created_at')
    serializer_class = LogActionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduledTaskViewSet(mixins.ListModelMixin, 
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):

    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        tasks = ScheduledTask.objects.all()
        titles = ScheduledTask.title_choices
        if len(tasks) != len(titles):
            task_titles = []
            admin = User.objects.filter(is_staff=True).first()
            for task in tasks:
                task_titles.append(task.task.name)
            for title in titles:
                if title[0] not in task_titles:
                    path_task = 'actions.tasks.' + title[0]
                    schedule, _ = CrontabSchedule.objects.get_or_create(minute='0',
                                                                        hour='8',
                                                                        day_of_week='1',
                                                                        day_of_month='*',
                                                                        month_of_year='*')
                    task = PeriodicTask.objects.create(crontab=schedule, name=title[0], task=path_task, enabled=False)
                    ScheduledTask.objects.create(title=title[0], enabled=False, time='00-08-01-**', task=task, admin=admin)
            tasks = ScheduledTask.objects.all()
        
        serializer = ScheduledTaskSerializer(tasks, many=True)
        return Response(serializer.data)