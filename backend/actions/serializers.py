from rest_framework import serializers
from actions.models import LogAction, Action, ScheduledTask
from django.contrib.auth.models import User
import os
import pathlib

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
    
    def validate_template(self, value):
        path = str(pathlib.Path(__file__).parent.absolute() / 'ansible' / 'project') + os.sep + value
        if not os.path.isfile(path):
            raise serializers.ValidationError("Invalid template, must be previously created in ansible folder")
        return value

class LogActionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    action = ActionSerializer(required=True)
    class Meta:
        model = LogAction
        exclude = ['updated_at']


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''
        for val in self._choices:
            if self._choices[val] == data or val == data:
                return val
        self.fail('invalid_choice', input=data)

class ScheduledTaskSerializer(serializers.ModelSerializer):
    time = serializers.CharField(max_length=11)
    title = ChoiceField(choices=ScheduledTask.title_choices)
    admin = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = ScheduledTask
        exclude = ['task']
    
    def validate_time(self, value):
        error = "Please introduce the schedule with the following format: <mm-hh-dd-mm> where d=dayofweek and m=dayofmonth. If a field is all please use <**>"
        minute = value[0:2]
        hour = value[3:5]
        day_of_week = value[6:8]
        day_of_month = value[9:11]
        list = [minute, hour, day_of_week, day_of_month]
        limits = [59, 24, 7, 28]
        for i, time in enumerate(list):
            if not time.isdigit() and time != '**':
                raise serializers.ValidationError(error)
            elif time.isdigit():
                if int(time) > limits[i]:
                    raise serializers.ValidationError(error)
        return value