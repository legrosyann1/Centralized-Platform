from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask


class Action(models.Model):
    name = models.CharField(max_length=100)
    template = models.CharField(max_length=100)

    def __str__(self):
        return '{} using template {}'.format(self.name, self.template)

class LogAction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.CharField(max_length=512)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    def __str__(self):
        return '{} executed by {} at {}'.format(self.action.name, self.user.get_full_name(), self.created_at)


class ScheduledTask(models.Model):
    # first item of tuple must be the name of the periodic task
    title_choices = [
        ('helloWorld', 'Hello World'),
        ('getWeeklyChanges', 'Weekly changes in all devices')
    ]
    title = models.CharField(max_length=70, choices=title_choices)
    enabled = models.BooleanField(default=False)
    time = models.CharField(max_length=11)
    task = models.OneToOneField(PeriodicTask,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)