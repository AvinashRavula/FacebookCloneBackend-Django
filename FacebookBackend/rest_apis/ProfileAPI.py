from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.serializers import User

from FacebookBackend.models import Profile
from FacebookBackend.serializers.ProfileSerializer import ProfileSerializer
from FacebookBackend.serializers.UserSerializer import UserSerializer


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def update(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs.get('pk'))
        if self.request.user.id == profile.user.id:
            m_data = request.data
            m_data['phonenum'] = profile.phonenum
            m_data['user'] = profile.user.id
            serializer = ProfileSerializer(profile, data=m_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'you dont have permission to do this...'})


@api_view(['GET'])
def duplicate_phonenum(request):
    if request.method == 'GET':
        print(request.GET['phonenum'])
        profile = Profile.objects.all().filter(phonenum=request.GET['phonenum'])
        if len(profile) == 0:
            return JsonResponse({'phonenum': '%s' % request.GET['phonenum']})
        return JsonResponse({'phonenum': 'invalid'})
