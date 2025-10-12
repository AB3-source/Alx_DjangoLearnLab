from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

# after request.user.follow(target)
if target != request.user:
    Notification.objects.create(
        recipient=target,
        actor=request.user,
        verb='followed',
        target_content_type=ContentType.objects.get_for_model(request.user.__class__),
        target_object_id=str(request.user.id),
        data={'follower_username': request.user.username}
    )


# --- Follow / Unfollow functionality --- #
class FollowUserView(generics.GenericAPIView):
    """
    Allow a user to follow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # using CustomUser.objects.all()
        queryset = User.objects.all()
        target = get_object_or_404(queryset, id=user_id)

        if target == request.user:
            return Response({'detail': "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.follow(target)
        return Response({
            'detail': f'You are now following {target.username}.',
            'following_count': request.user.following.count(),
            'target_followers_count': target.followers.count()
        }, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Allow a user to unfollow another user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        queryset = User.objects.all()  
        target = get_object_or_404(queryset, id=user_id)

        if target == request.user:
            return Response({'detail': "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.unfollow(target)
        return Response({
            'detail': f'You have unfollowed {target.username}.',
            'following_count': request.user.following.count(),
            'target_followers_count': target.followers.count()
        }, status=status.HTTP_200_OK)
