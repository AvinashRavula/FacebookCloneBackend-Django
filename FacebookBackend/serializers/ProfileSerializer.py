from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from FacebookBackend.models import Profile
from FacebookBackend.serializers.FileUploadSerializer import ProfilePictureSerializer, CoverPictureSerializer


class ProfileSerializer(ModelSerializer):
    # profile_picture = serializers.CharField(source="profilepicture.id", read_only=True)
    # cover_picture = serializers.CharField(source="CoverPicture.id", read_only=True)
    profilepicture = ProfilePictureSerializer(read_only=True)
    coverpicture = CoverPictureSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'nick_name', 'dob', 'phonenum', 'gender',
                  'born_place', 'languages_known', 'relationship_status', 'user',
                  'profilepicture', 'coverpicture']

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
