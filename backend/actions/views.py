from rest_framework import viewsets, generics, permissions
from actions.models import LogAction, Action, ScheduledTask
from actions.serializers import LogActionSerializer, ActionSerializer, ScheduledTaskSerializer
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework.response import Response

# Create your views here.

class ActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [permissions.IsAuthenticated]

class LogActionsViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = LogAction.objects.all()
    serializer_class = LogActionSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduledTaskViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):

    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        tasks = ScheduledTask.objects.all()
        if len(tasks) == 0:
            titles = ScheduledTask.title_choices
            for title in titles:
                path_task = 'actions.tasks.' + title[0]
                schedule, _ = CrontabSchedule.objects.get_or_create(minute='00',hour='8',day_of_week='1',day_of_month='*',month_of_year='*')
                task = PeriodicTask.objects.create(crontab=schedule, name=title[0], task=path_task, enabled=False)
                ScheduledTask.objects.create(title=title[0], enabled=False, time='00-08-01-**', task=task)
            tasks = ScheduledTask.objects.all()
        
        serializer = ScheduledTaskSerializer(tasks, many=True)
        return Response(serializer.data)