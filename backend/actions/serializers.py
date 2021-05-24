from rest_framework import serializers
from actions.models import LogAction, Action, ScheduledTask
from django.contrib.auth.models import User

class ActionSerializer(serializers.ModelSerializer):
    template = serializers.FileField(use_url=False, required=True)
    class Meta:
        model = Action
        fields = '__all__'

class LogActionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    action = ActionSerializer(required=True)
    class Meta:
        model = LogAction
        fields = '__all__'


class ScheduledTaskSerializer(serializers.ModelSerializer):
    time = serializers.CharField(max_length=11)
    class Meta:
        model = ScheduledTask
        exclude = ['task']
    
    def validate_time(self, value):
        minute = value[0:2]
        hour = value[3:5]
        day_of_week = value[6:8]
        day_of_month = value[9:11]
        list = [minute, hour, day_of_week, day_of_month]
        limits = [60, 24, 7, 28]
        for i, time in enumerate(list):
            if not time.isdigit() and time != '**':
                raise serializers.ValidationError("Please introduce the schedule with the following format: <mm-hh-dd-mm> where d=dayofweek and m=dayofmonth. If a field is all please use <**>")
            elif time.isdigit():
                if int(time) > limits[i]:
                    raise serializers.ValidationError("Please introduce the schedule with the following format: <mm-hh-dd-mm> where d=dayofweek and m=dayofmonth. If a field is all please use <**>")
        return value