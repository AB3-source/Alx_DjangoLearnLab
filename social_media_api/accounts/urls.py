# accounts/urls.py
from django.urls import path
from .views import RegisterView, CustomObtainAuthToken, ProfileView
# import the new follow views
from .views import FollowUserView, UnfollowUserView, FollowingListView, FollowersListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Follows
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/<int:user_id>/', FollowingListView.as_view(), name='user-following'),
    path('following/', FollowingListView.as_view(), name='my-following'),
    path('followers/<int:user_id>/', FollowersListView.as_view(), name='user-followers'),
    path('followers/', FollowersListView.as_view(), name='my-followers'),
]
