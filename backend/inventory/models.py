from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
import os
from django.core.files.storage import FileSystemStorage

class LogicPartition(models.Model):
    name = models.CharField(max_length=100)

class Device(models.Model):
    status_choices = [
        ('stable', 'Stable'),
        ('unstable', 'Unstable'),
        ('critical', 'Critical')
    ]
    mode_choices = [
        ('active', 'Active'),
        ('down', 'Down')
    ]

    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False)
    mac_address = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=100, null=True)
    serial_number = models.CharField(max_length=100, null=True, unique=True)
    mode = models.CharField(max_length=30, choices=mode_choices, default='down')
    status = models.CharField(max_length=30, choices=status_choices, default='stable')
    manufacturer = models.CharField(max_length=100, null=True)
    operating_system = models.CharField(max_length=30, null=True)
    sw_version = models.CharField(max_length=30, null=True)
    hw_end_of_life = models.DateTimeField(null=True)
    sw_end_of_life = models.DateTimeField(null=True)
    logic_partition = models.ManyToManyField(LogicPartition, blank=True)
    zone = models.CharField(max_length=30, null=True)
    area = models.CharField(max_length=30, null=True)
    group = models.CharField(max_length=50, null=True)
    fqdn = models.CharField(max_length=300, null=True)
    contact_person = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.ip_address} - {self.name}'


class Interface(models.Model):
    status_choices = [
        ('connected', 'Connected'),
        ('not_connected', 'Not connected'),
        ('disabled', 'Disabled')
    ]
    name = models.CharField(max_length=100, null=True)
    ip_address = models.GenericIPAddressField(null=True)
    status = models.CharField(max_length=100, choices=status_choices, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='interfaces')


class DeviceComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return '{} -- {} -- {}'.format(self.device, self.user, self.comment)


class Change(models.Model):
    change_code = models.CharField(max_length=50, null=True)
    old_info = models.JSONField()
    new_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Verify if files directory exists, if not, create it
store = Path('/inventory/files/changes/')
path = str(Path(__file__).parent.absolute().parent) + str(store)
if os.path.isdir(path):
    pass
else:
    os.makedirs(path)

fs = FileSystemStorage(location=path)
class FutureChange(models.Model):
    type_choices = [
        ('corrective', 'Corrective'),
        ('evolutionary', 'Evolutionary'),
        ('pre-approved', 'Pre-approved')
    ]
    state_choices = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
        ('incompleted', 'Incompleted')
    ]

    change_code = models.CharField(max_length=13, unique=True) #CH<2digitnumber>-<day><month><year>
    implementer = models.ForeignKey(User, on_delete=models.CASCADE)
    requester = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    environment = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=20, choices=state_choices, null=True, blank=True)
    type = models.CharField(max_length=50, choices=type_choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_urgent = models.BooleanField(default=False, null=True, blank=True)
    #rfc = models.FileField(upload_to='changes/%Y/%m', null=True)
    rfc = models.FileField(storage=fs, null=True, blank=True, max_length=None)