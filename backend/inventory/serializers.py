from .models import Device
from rest_framework import serializers


class DevicesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ['ip_address', 'name']