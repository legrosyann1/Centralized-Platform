from django.contrib.auth.models import User, Group
from .models import UserProfile
from rest_framework import serializers

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
        user_data = validated_data.pop('user')
        group_data = user_data.pop('groups')
        user = User.objects.create(**user_data)  
        user.set_password(user_data['password'])    
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
        user_data = validated_data.pop('user')
        user = instance.user

        for key in validated_data:
            setattr(instance, key, validated_data[key])
        instance.save()

        for key in user_data:
            if key == 'groups':
                for group in user_data[key]:
                    new_group = Group.objects.get_or_create(name = group)
                    user.groups.add(new_group)
            elif key == 'id':
                pass
            elif key == 'password':
                user.set_password(user_data[key])
            else:
                setattr(user, key, user_data[key])
        user.save()

        return instance


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
