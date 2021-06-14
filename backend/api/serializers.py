from django.contrib.auth.models import User, Group
from .models import UserProfile
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'first_name', 'last_name', 'is_staff', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'username': {'validators': []}}

    def validate_username(self, value):
        if self.context['request']._request.method == 'POST':
           if self.Meta.model.objects.filter(username=value).exists():
               raise serializers.ValidationError('A username with this name already exists.')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['id', 'viewTour', 'user'] 

    def create(self, validated_data):
        data_user = validated_data.pop('user')
        group_data = data_user.pop('groups')
        user = User.objects.create(**data_user)  
        user.set_password(data_user['password'])    
        for group in group_data:
            new_group = Group.objects.get_or_create(name = group)
            user.groups.add(new_group)
        user.save()

        profile = UserProfile.objects.get(user=user)
        for key in validated_data:
            setattr(profile, key, validated_data[key])
        profile.save()
        return profile

    def update(self, instance, validated_data):
        data_user = validated_data.pop('user')
        user = instance.user
        if (self.context['request'].user.is_superuser and 
            self.context['request'].user.username != data_user['username']):
            current_user = User.objects.get(username=data_user['username'])
        else:
            current_user = self.context['request'].user
        if (not current_user.is_superuser and 
            current_user.username != data_user['username']):
            raise PermissionDenied()
        elif not current_user.check_password(data_user['password']):
            raise AuthenticationFailed()

        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()
        for key in data_user:
            if key == 'groups':
                for group in data_user[key]:
                    new_group = Group.objects.get_or_create(name = group)
                    user.groups.add(new_group)
            elif key == 'id' or key == 'password':
                pass
            else:
                setattr(user, key, data_user[key])
        user.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
