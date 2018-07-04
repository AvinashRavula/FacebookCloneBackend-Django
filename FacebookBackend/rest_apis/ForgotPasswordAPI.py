from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from FacebookBackend.models import Profile
from FacebookBackend.serializers.UserSerializer import UserSerializer
from FacebookBackend.views.UserForm import UserForm


@api_view(['GET'])
def get_user_id(request):
    if request.method == 'GET':
            if request.GET['key'].isdigit():
                user = Profile.objects.values('user','user__username').filter(phonenum=request.GET['key'])
            
                if len(user) > 0:
                    return JsonResponse({'id': user[0].get('user'),'username':  user[0].get('user__username')})
            else:
                user = User.objects.values('id','username').filter(email=request.GET['key'])
                if len(user) > 0:
                    return JsonResponse({'id': user[0].get('id'),'username': user[0].get('username')})
            return JsonResponse({'error': 'User not found'})


@api_view(['POST'])
def change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        user_id = request.POST['user']
        user = get_object_or_404(User, pk=user_id)
        user_form = UserForm(request.POST, instance=user)
        if user:
            user = user_form.save()
            user.set_password(password)
            user.save()
            return JsonResponse({'password_changed': True})
        return JsonResponse({'password_changed': False})
