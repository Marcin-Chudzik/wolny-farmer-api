"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.utils import (
    create_user,
    create_post,
)


class ModelTests(TestCase):
    """Test models."""

    def setUp(self):
        self.user = create_user()
        self.user_payload = {
            'email': 'test@example.com',
            'password': 'sample123'
        }
        self.post_payload = {
            'title': 'Test title',
            'body': 'Test body',
            'author': self.user
        }

    """USER MODEL"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful."""
        user = create_user(**self.user_payload)

        self.assertEqual(user.email, self.user_payload['email'])
        self.assertTrue(user.check_password(self.user_payload['password']))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['testa@EXAMPLE.com', 'testa@example.com'],
            ['Testb@Example.com', 'Testb@example.com'],
            ['TESTc@EXAMPLE.COM', 'TESTc@example.com'],
            ['testd@example.COM', 'testd@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='sample123'
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_user(superuser=True)

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    """POST MODEL"""

    def test_create_post_success(self):
        """Test creating a new post with provided data."""
        post = create_post(**self.post_payload)

        self.assertEqual(post.title, self.post_payload['title'])
        self.assertEqual(post.body, self.post_payload['body'])
        self.assertEqual(post.author, self.post_payload['author'])

    def test_creating_new_post_required_data(self):
        """Test creating a new post with empty fields return error."""
        payload = {
            'title': '',
            'body': '',
            'author': '',
        }

        with self.assertRaises(ValueError):
            post = create_post(**payload)
            post.full_clean()
