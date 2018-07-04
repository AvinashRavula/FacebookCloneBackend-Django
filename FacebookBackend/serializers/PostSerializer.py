from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from FacebookBackend.models import Post
from FacebookBackend.serializers.FileUploadSerializer import AttachmentLinksSerializer


# class PostSerializer(ModelSerializer):
#
#     class Meta:
#         model = Post
#         fields = ['id', 'captions', 'tagged_ids', 'likes_ids', 'user']
from FacebookBackend.serializers.all_serializers import CommentSerializer


class PostSerializer(ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    attachments = AttachmentLinksSerializer(read_only=True, many=True, source="attachmentlinks_set")
    comments = CommentSerializer(read_only=True, many=True, source="comment_set")

    class Meta:
        model = Post
        fields = ['id', 'captions', 'tagged_ids', 'likes_ids', 'created_time',
                  'user', 'first_name', 'last_name', 'comments', 'attachments']
