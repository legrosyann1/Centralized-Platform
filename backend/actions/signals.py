from django.db.models.signals import pre_save
from django.dispatch import receiver
from actions.models import ScheduledTask
from django_celery_beat.models import CrontabSchedule, PeriodicTask


@receiver(pre_save, sender=ScheduledTask)
def updateScheduledTask(sender, instance, **kwargs):
    print('here')
    minute, hour, day_of_week, day_of_month = parse_time(instance.time)
    print(instance.id)
    if instance.id is not None:
        schedtask = ScheduledTask.objects.get(id=instance.id)
        task = schedtask.task
        task.enabled = instance.enabled
        schedule = CrontabSchedule.objects.get(id=task.crontab_id)
        schedule.minute = minute
        schedule.hour = hour
        schedule.day_of_week = day_of_week
        schedule.day_of_month = day_of_month
        schedule.save()
        task.crontab = schedule
        task.save()
    
def parse_time(time):
    scheds = time.split('-')
    times = []
    for sched in scheds:
        if '**' in sched:
            times.append('*')
        else:
            times.append(str(int(sched)))
    minute = times[0]
    hour = times[1]
    day_of_week = times[2]
    day_of_month = times[3]
    return minute, hour, day_of_week, day_of_month