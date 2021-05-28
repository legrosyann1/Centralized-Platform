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
    class Meta:
        model = ScheduledTask
        exclude = ['task']
    
    def validate_time(self, value):
        minute = value[0:2]
        hour = value[3:5]
        day_of_week = value[6:8]
        day_of_month = value[9:11]
        list = [minute, hour, day_of_week, day_of_month]
        limits = [59, 24, 7, 28]
        for i, time in enumerate(list):
            if not time.isdigit() and time != '**':
                raise serializers.ValidationError("Please introduce the schedule with the following format: <mm-hh-dd-mm> where d=dayofweek and m=dayofmonth. If a field is all please use <**>")
            elif time.isdigit():
                if int(time) > limits[i]:
                    raise serializers.ValidationError("Please introduce the schedule with the following format: <mm-hh-dd-mm> where d=dayofweek and m=dayofmonth. If a field is all please use <**>")
        return value