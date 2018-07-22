from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from FacebookBackend.models import Post, Friends
from FacebookBackend.serializers.PostSerializer import PostSerializer

from rest_framework.pagination import PageNumberPagination


class PostSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-last_modified')
    pagination_class = PostSetPagination

    def create(self, request, *args, **kwargs):
        req_data = request.data
        req_data['user'] = self.request.user.id
        serializer = self.serializer_class(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        if self.request.user.id == post.user.id:
            m_data = request.data
            m_data['user'] = post.user.id
            serializer = PostSerializer(post, data=m_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error': 'you dont have permission to do this...'})


@api_view(['put'])
def like_a_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        user_id = str(request.user.id)
        likes_ids = []
        try:
            likes_ids = post.likes_ids.split(",")
        except AttributeError:
            pass
        likes_ids = [value for value in likes_ids if value != '']
        if user_id not in likes_ids:
            likes_ids.append(user_id)
            serializer = PostSerializer(post, data={'likes_ids': ",".join(likes_ids), 'user': post.user.id})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['put'])
def unlike_a_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        user_id = str(request.user.id)
        likes_ids = []
        try:
            likes_ids = post.likes_ids.split(",")
        except AttributeError:
            pass
        likes_ids = [value for value in likes_ids if value != '']
        if user_id in likes_ids:
            likes_ids.remove(user_id)
            serializer = PostSerializer(post, data={'likes_ids': ",".join(likes_ids), 'user': post.user.id})
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class NewsFeedAPI(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostSetPagination

    def get_queryset(self):
        friends = Friends.objects.all().filter(Q(friend=self.request.user.id) | Q(user=self.request.user.id))
        friends = friends.exclude(status=0)
        friend_list = [friend.user.id for friend in friends]
        friend_list2 = [friend.friend.id for friend in friends]
        friend_list.extend(friend_list2)
        friend_list.__add__(self.request.user.id)
        friend_list = list(set(friend_list))
        return Post.objects.filter(user__in=friend_list).order_by('-last_modified')
