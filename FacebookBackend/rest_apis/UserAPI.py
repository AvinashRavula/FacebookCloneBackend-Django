from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from FacebookBackend.serializers.UserSerializer import UserSerializer
from FacebookBackend.serializers.all_serializers import UserProfileSerializer
from FacebookBackend.views.UserForm import UserForm

class UserSearchAPI(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        users = User.objects.filter(Q(last_name__icontains=self.request.GET['query']) | 
                               Q(first_name__icontains=self.request.GET['query']))
        return users.exclude(id=self.request.user.id)


# version 2
class UserProfileAPI(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


# version 2
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# version 1
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# version 1
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        username = self.kwargs["username"]
        obj = get_object_or_404(User, username=username)
        return obj

    # def update(self, request, *args, **kwargs):
    #     import ipdb
    #     ipdb.set_trace()
    #     user = get_object_or_404(User, **kwargs)
    #     user_form = UserForm(request.POST, instance=user)
    #     if user:
    #         user = user_form.save()
    #         user.set_password(request.data.get('password'))
    #         user.save()
    #         return JsonResponse({'updated': True})
    #     return JsonResponse({'updated': False})


@api_view(['GET'])
def duplicate_email_address(request):
    if request.method == 'GET':
        print(request.GET['email'])
        user = User.objects.all().filter(email=request.GET['email'])
        if len(user) == 0:
            return JsonResponse({'email': '%s' % request.GET['email']})
        return JsonResponse({'email': 'invalid'})
