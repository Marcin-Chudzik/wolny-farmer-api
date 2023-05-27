"""
Tests for the blog API.
"""
from datetime import datetime

from core.models import Post
from core.utils import (
    create_user,
    create_post,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_POST_URL = reverse('blog:post-list')


class BlogAPITests(TestCase):
    """Tests for features of the blog API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(superuser=True)
        self.client.force_authenticate(self.user)
        self.today = datetime.today().strftime('%Y-%m-%d')

        self.payload = {
            'title': 'Test title',
            'body': 'hamsters likes nutella of course.',
            'publish': self.today,
        }

    def test_only_superuser_can_create_post(self):
        """Test if only superuser can create a post."""
        self.client.force_authenticate(None)
        self.client.force_authenticate(create_user())
        res = self.client.post(CREATE_POST_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        post_exists = Post.objects.filter(
            title=self.payload['title'],
            publish=self.today
        ).exists()
        self.assertFalse(post_exists)

    def test_create_post_success(self):
        """Test creating a post is successfully."""
        res = self.client.post(CREATE_POST_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(
            title=self.payload['title'],
        )
        self.assertEqual(post.title, self.payload['title'])
        self.assertEqual(post.body, self.payload['body'])

    def test_post_with_title_exists_error(self):
        """Test an error is returned if post with the same
           title and status "publish" exists."""
        create_post(**self.payload)
        res = self.client.post(CREATE_POST_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        posts = Post.objects.filter(
            title=self.payload['title'],
            publish=self.today
        )
        self.assertEqual(posts.count(), 1)

    def test_title_or_body_too_short_error(self):
        """Test an error occurred if post title or body are too short."""
        payload = {
            'title': 'Test',
            'body': 'Test',
            'author': self.user.id
        }
        res = self.client.post(CREATE_POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        post_exists = Post.objects.filter(
            title=payload['title'],
            publish=self.today
        ).exists()
        self.assertFalse(post_exists)
