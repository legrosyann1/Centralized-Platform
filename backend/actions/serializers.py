from rest_framework import serializers
from actions.models import LogAction, Action
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