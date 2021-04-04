from django.db import models

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

    ip_address = models.CharField(max_length=30, null=True)
    mac_address = models.CharField(max_length=30, null=True)
    name = models.CharField(max_length=100, null=True)
    serial_number = models.CharField(max_length=100, null=True, unique=True)
    create_time = models.BigIntegerField(null=True)
    updated_device_time = models.DateTimeField(null=True)
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

    def __str__(self):
        return f'{self.ip_address} - {self.name}'

class DevicesComment(models.Model):
    user = models.CharField(max_length = 50)
    comment = models.TextField(null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return '{} -- {} -- {}'.format(self.device, self.user, self.comment)
