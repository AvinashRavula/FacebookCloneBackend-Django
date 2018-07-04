from django.db.migrations import serializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from FacebookBackend.models import ProfilePicture, AttachmentLinks, CoverPicture


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = ['id', 'image', 'profile']


class CoverPictureSerializer(ModelSerializer):
    class Meta:
        model = CoverPicture
        fields = ['id', 'image', 'profile']


class AttachmentLinksSerializer(ModelSerializer):
    class Meta:
        model = AttachmentLinks
        fields = ('id', 'file', 'type', 'post')
