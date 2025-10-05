from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm


# -------------------------
# Post Views (List, Detail, Create, Update, Delete)
# -------------------------

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        # assign author, save post, then handle tags
        form.instance.author = self.request.user
        response = super().form_valid(form)  # saves self.object
        tags_str = form.cleaned_data.get("tags", "")
        self._attach_tags(self.object, tags_str)
        return response

    def _attach_tags(self, post, tags_str):
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        tag_objs = []
        for name in tags:
            tag_obj, _created = Tag.objects.get_or_create(name__iexact=False, name=name)
            # get_or_create ignores case only if custom logic; keep unique by exact name
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def get_initial(self):
        initial = super().get_initial()
        # Pre-fill tags field with comma-separated tag names
        initial["tags"] = ", ".join([t.name for t in self.get_object().tags.all()])
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)  # saves self.object
        tags_str = form.cleaned_data.get("tags", "")
        self._attach_tags(self.object, tags_str)
        return response

    def _attach_tags(self, post, tags_str):
        tags = [t.strip() for t in tags_str.split(",") if t.strip()]
        tag_objs = []
        for name in tags:
            tag_obj, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)
        post.tags.set(tag_objs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# -------------------------
# Comment Views (Create handled via separate view, plus Update/Delete)
# -------------------------

# Create comment via function view for simplicity (used by post detail form)
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "There was a problem with your comment.")
    return redirect("post-detail", pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# -------------------------
# Tagging and Search Views
# -------------------------

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()
    return render(request, "blog/posts_by_tag.html", {"tag": tag, "posts": posts})


def search(request):
    q = request.GET.get("q", "").strip()
    results = Post.objects.none()
    if q:
        results = Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()
    return render(request, "blog/search_results.html", {"query": q, "results": results})
