from .models import Device, DevicesComment, LogicPartition
from rest_framework import serializers
from datetime import datetime

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
            modified = False
            if dev_obj is not None:
                for field in reversed(fields):
                    if (device.get(field.name) is not None) and (device.get(field.name) != getattr(dev_obj, field.name)):
                        modified = True
                        setattr(dev_obj, field.name, device[field.name])
                        setattr(dev_obj, 'updated_device_time', datetime.now())
            else:
                dev_obj = Device.objects.create(**device)
            if modified:
                dev_obj.save()
            dev_list.append(dev_obj)
        return dev_list


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        list_serializer_class = DeviceListSerializer
        #depth = 1
        fields = '__all__'
        #exclude = ['created_at']
        

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevicesComment
        fields = "__all__"
