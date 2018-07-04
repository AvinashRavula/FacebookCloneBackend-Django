from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from FacebookBackend.models import ProfilePicture, AttachmentLinks, CoverPicture
from FacebookBackend.serializers.FileUploadSerializer import ProfilePictureSerializer, AttachmentLinksSerializer, \
    CoverPictureSerializer


class ProfilePictureViewSet(viewsets.ModelViewSet):
    queryset = ProfilePicture.objects.all()
    serializer_class = ProfilePictureSerializer


class CoverPictureViewSet(viewsets.ModelViewSet):
    queryset = CoverPicture.objects.all()
    serializer_class = CoverPictureSerializer


class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = AttachmentLinks.objects.all()
    serializer_class = AttachmentLinksSerializer
