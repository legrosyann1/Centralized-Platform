from .models import Device, DeviceComment, LogicPartition, Change, FutureChange
from django.contrib.auth.models import User
from rest_framework import serializers

class LogicPartitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogicPartition
        fields = '__all__'

class DeviceListSerializer(serializers.ListSerializer):
    def create(self, devices):
        '''
        This function is called when many=True parameter is received. 
        It gets devices list as a parameter with dict format.
        It retrieves the actual devices from db and iterate over it's fields 
        to update this fields
        If the device is not created then create a new one.
        '''
        fields = Device._meta.get_fields()
        dev_list = []
        for device in devices:
            dev_obj = Device.objects.filter(ip_address=device['ip_address']).first()
            if dev_obj is not None:
                for field in reversed(fields):
                    if (device.get(field.name) is not None) and (device.get(field.name) != getattr(dev_obj, field.name)):
                        setattr(dev_obj, field.name, device[field.name])
                dev_obj.save()
            else:
                logPartitions = device.pop('logic_partition')
                dev_obj = Device.objects.create(**device)
                for part in logPartitions:
                    dev_obj.logic_partition.add(part)
            dev_list.append(dev_obj)
        return dev_list


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        list_serializer_class = DeviceListSerializer
        exclude = ['created_at']
        

class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = DeviceComment
        fields = ['id','user','comment','device']


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Change
        fields = '__all__'


class FutureChangeSerializer(serializers.ModelSerializer):
    implementer = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    rfc = serializers.FileField(use_url=False, max_length=None, required=False, allow_null=True)
    class Meta:
        model = FutureChange
        fields = '__all__'