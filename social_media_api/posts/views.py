from rest_framework import status, permissions, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from notifications.models import Notification

class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        # prevent liking own post? (optional) we allow liking own post
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # create a notification for the post author (if not liking your own post)
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked',
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=str(post.id),
                data={'post_title': post.title}
            )

        return Response({'detail': 'Post liked.', 'likes_count': post.likes.count()}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post.objects.all(), pk=pk)
        try:
            like = Like.objects.get(post=post, user=request.user)
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({'detail': 'Post unliked.', 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)
# in CommentViewSet.perform_create
comment = serializer.save(author=self.request.user)
if comment.post.author != self.request.user:
    Notification.objects.create(
        recipient=comment.post.author,
        actor=self.request.user,
        verb='commented',
        target_content_type=ContentType.objects.get_for_model(comment),
        target_object_id=str(comment.id),
        data={'comment_excerpt': comment.content[:100], 'post_id': comment.post.id}
    )
