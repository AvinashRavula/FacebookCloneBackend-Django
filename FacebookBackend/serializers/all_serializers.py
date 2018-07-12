from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from FacebookBackend.models import CoverPicture, Languages, Gender, Comment, Reply, Friends, LinkedAccount
from FacebookBackend.serializers.ProfileSerializer import ProfileSerializer


class LinkedAccountSerializer(ModelSerializer):
    class Meta:
        model = LinkedAccount
        fields = ['id', 'name', 'link', 'profile']


class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Languages
        fields = ['id', 'name']


class GenderSerializer(ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'post', 'like_ids',  'comment_by']


class ReplySerializer(ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'reply_text', 'like_ids', 'reply_ids', 'comment', 'replied_by']


class FriendsSerializer(ModelSerializer):
    class Meta:
        model = Friends
        fields = ['id', 'user', 'friend', 'status']


class UserProfileSerializer(ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']
