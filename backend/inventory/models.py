from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Name')
    ip_address = models.CharField(max_length=30, null=True, verbose_name='IP Address')
