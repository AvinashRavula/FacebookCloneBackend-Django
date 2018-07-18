from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from FacebookBackend.serializers.FileUploadSerializer import ProfilePictureSerializer


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.IntegerField(source="profile.id", read_only=True)
    profilepicture = serializers.CharField(source='profile.profilepicture.image', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password', 'profile', 'profilepicture')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
