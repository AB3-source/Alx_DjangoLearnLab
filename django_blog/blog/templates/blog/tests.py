# blog/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.other = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(title='T', content='C', author=self.user)

    def test_list_view(self):
        resp = self.client.get(reverse('post-list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)

    def test_create_requires_login(self):
        resp = self.client.get(reverse('post-create'))
        self.assertRedirects(resp, '/login/?next=' + reverse('post-create'))

        self.client.login(username='alice', password='pass')
        resp = self.client.post(reverse('post-create'), {'title':'New','content':'Body'})
        self.assertEqual(Post.objects.count(), 2)

    def test_update_only_author(self):
        self.client.login(username='bob', password='pass')
        resp = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(resp.status_code, 403)  # or redirect depending on mixin behavior

    def test_delete_only_author(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.post(reverse('post-delete', args=[self.post.pk]))
        self.assertRedirects(resp, reverse('post-list'))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
