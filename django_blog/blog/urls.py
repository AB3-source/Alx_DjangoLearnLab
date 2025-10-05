from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    add_comment, CommentUpdateView, CommentDeleteView,
    posts_by_tag, search
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # comments
    path("post/<int:pk>/comments/new/", add_comment, name="add-comment"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),

    # tags and search
    path("tags/<str:tag_name>/", posts_by_tag, name="posts-by-tag"),
    path("search/", search, name="search"),
]
