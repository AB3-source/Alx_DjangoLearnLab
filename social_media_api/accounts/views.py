# accounts/views.py (add these imports at top if not present)
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follow(target)  # uses model helper
        return Response({
            'detail': f'You are now following {target.username}.',
            'following_count': request.user.following.count(),
            'target_followers_count': target.followers.count()
        }, status=status.HTTP_200_OK)

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.unfollow(target)
        return Response({
            'detail': f'You have unfollowed {target.username}.',
            'following_count': request.user.following.count(),
            'target_followers_count': target.followers.count()
        }, status=status.HTTP_200_OK)

class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id=None):
        """
        If user_id is provided, show following for that user (publicly visible).
        Otherwise show the authenticated user's following.
        """
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        # serialize minimal info
        data = [{'id': u.id, 'username': u.username} for u in user.following.all()]
        return Response({'user': user.username, 'following': data})

class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        data = [{'id': u.id, 'username': u.username} for u in user.followers.all()]
        return Response({'user': user.username, 'followers': data})
