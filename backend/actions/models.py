from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django_celery_beat.models import PeriodicTask
from pathlib import Path
import os


store = Path('/actions/ansible/')
path = str(Path(__file__).parent.absolute().parent) + str(store)
if os.path.isdir(path):
    pass
else:
    os.makedirs(path)

fs = FileSystemStorage(location=path)
class Action(models.Model):
    name = models.CharField(max_length=100)
    template = models.FileField(storage=fs, max_length=None)

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
    title_choices = [
        ('hello', 'Hello')
    ]
    title = models.CharField(max_length=70, choices=title_choices)
    enabled = models.BooleanField(default=False)
    time = models.CharField(max_length=11)
    task = models.OneToOneField(PeriodicTask,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)