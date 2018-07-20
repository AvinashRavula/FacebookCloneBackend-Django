from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from FacebookBackend.rest_apis.ForgotPasswordAPI import get_user_id, change_password
from FacebookBackend.rest_apis.PostAPI import PostViewSet, like_a_post, unlike_a_post
from FacebookBackend.rest_apis.ProfileAPI import ProfileList, ProfileDetail, ProfileViewSet
from FacebookBackend.rest_apis.UserAPI import UserList, duplicate_email_address, UserDetail, UserViewSet, UserProfileAPI, \
    UserSearchAPI
from FacebookBackend.rest_apis.ProfileAPI import duplicate_phonenum
from FacebookBackend.rest_apis.FileUploadAPI import *
from FacebookBackend.rest_apis.otherapis import LinkedAccountViewSet, LanguageViewSet, GenderViewSet, CommentViewSet, \
    ReplyViewSet, FriendsViewSet, FriendRequestsAPI, PeopleYouMayKnowAPI, MyFriendsAPI

router = routers.DefaultRouter()
router.register('dps', ProfilePictureViewSet, 'dps')
router.register('cps', CoverPictureViewSet, 'cps')
router.register('files', FileUploadViewSet, 'files')
router.register('posts', PostViewSet, 'posts')
router.register('linkedaccounts', LinkedAccountViewSet, 'linkedaccounts')
router.register('languages', LanguageViewSet, 'languages')
router.register('genders', GenderViewSet, 'genders')
router.register('comments', CommentViewSet, 'comments')
router.register('replies', ReplyViewSet, 'replies')
router.register('friends', FriendsViewSet, 'friends')
# router.register('friends/requests', FriendRequestsAPI.as_view(), 'friend_requests')

router_v2 = routers.DefaultRouter()
router_v2.register('users', UserViewSet, 'users')
router_v2.register('profiles', ProfileViewSet, 'profiles')


urlpatterns = [
    path('profiles', ProfileList.as_view(), name="profiles"),
    path('profiles/<int:pk>', ProfileDetail.as_view(), name="profiles"),
    path('users', UserList.as_view(), name="users"),
    path('users/<str:username>', UserDetail.as_view(), name="users"),
    path('duplicate_email/', duplicate_email_address, name="duplicate_email"),
    path('duplicate_phonenum/', duplicate_phonenum, name="duplicate_phonenum"),
    path('findUser', get_user_id, name="get_user_id"),
    path('change_password/', change_password, name="change_password"),
    path('posts/<int:pk>/like', like_a_post, name="like_a_post"),
    path('posts/<int:pk>/unlike', unlike_a_post, name="unlike_a_post"),
    path('friends/requests/', FriendRequestsAPI.as_view(), name='friend_requests'),
    path('peopleyoumayknow/', PeopleYouMayKnowAPI.as_view(), name='people_you_may_know'),
    path('my_friends/', MyFriendsAPI.as_view(), name='my_friends'),
    path('my_profile/', UserProfileAPI.as_view(), name='user_profile'),
    path('search_users/', UserSearchAPI.as_view(), name='user_search'),

    url(r'^api-jwt-token-auth/', obtain_jwt_token),
    url(r'^api-jwt-token-refresh/', refresh_jwt_token),
    url(r'^api-jwt-token-verify/', verify_jwt_token),
    url(r'^api-basictoken-auth/', obtain_auth_token),

    url(r'^', include(router.urls)),
    url(r'^v2/', include(router_v2.urls)),
]
