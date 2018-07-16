from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from FacebookBackend.models import Languages, Gender, LinkedAccount, Comment, Reply, Friends
from FacebookBackend.serializers.UserSerializer import UserSerializer
from FacebookBackend.serializers.all_serializers import LinkedAccountSerializer, LanguageSerializer, GenderSerializer, \
    FriendsSerializer, CommentSerializer, ReplySerializer
from django.db.models import Q


class LanguageViewSet(ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Languages.objects.all()


class GenderViewSet(ModelViewSet):
    serializer_class = GenderSerializer
    queryset = Gender.objects.all()


class LinkedAccountViewSet(ModelViewSet):
    serializer_class = LinkedAccountSerializer
    queryset = LinkedAccount.objects.all()


class FriendsViewSet(ModelViewSet):
    serializer_class = FriendsSerializer
    queryset = Friends.objects.all()

    # def get_queryset(self):
    #     return Friends.objects.filter(Q(user=self.request.user.id, status=1) | Q(friend=self.request.user.id, status=1))

    def create(self, request, *args, **kwargs):
        req_data = request.data
        req_data['user'] = self.request.user.id
        serializer = self.serializer_class(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        friends = get_object_or_404(Friends, **kwargs)
        req_data = request.data
        req_data['user'] = self.request.user.id
        req_data['friend'] = friends.friend.id
        serializer = self.serializer_class(friends, data=req_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class FriendRequestsAPI(ListAPIView):
    serializer_class = FriendsSerializer

    def get_queryset(self):
        return Friends.objects.all().filter(friend=self.request.user.id, status=0)


class PeopleYouMayKnowAPI(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.exclude(id=self.request.user.id)
        friends_requested = Friends.objects.values_list('friend').filter(user=self.request.user.id)
        friend_requests = Friends.objects.values_list('user').filter(friend=self.request.user.id)
        users = users.exclude(id__in=friend_requests)
        return users.exclude(id__in=friends_requested)
        # return User.objects.exclude(id__in=friends)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def create(self, request, *args, **kwargs):
        req_data = request.data
        req_data['comment_by'] = self.request.user.id
        serializer = self.serializer_class(data=req_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyViewSet(ModelViewSet):
    serializer_class = ReplySerializer
    queryset = Reply.objects.all()
