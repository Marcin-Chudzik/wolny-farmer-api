"""
Database models.
"""
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
)

"""Managers"""


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email: str, password: str,
                    **extra_fields) -> "User":
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(
            email=self.normalize_email(email),
            username=extra_fields.get('username', email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def promote_to_superuser(self, user: "User") -> None:
        """Change default user on superuser."""
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

    def create_superuser(self, email: str, password: str) -> "User":
        """Create and return a new superuser."""
        user = self.create_user(
            email=email,
            password=password,
        )
        self.promote_to_superuser(user)

        return user


class PublishManager(models.Manager):
    """Manager for posts."""

    def get_queryset(self):
        return super(PublishManager, self).get_queryset()\
            .filter(status='published')


"""Models"""


class User(AbstractUser, PermissionsMixin):
    """Custom user in the system."""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Post(models.Model):
    """Post for blog."""
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }

    title = models.CharField(
        max_length=255,
        unique_for_date='publish',
        blank=False, null=False
    )
    body = models.TextField(blank=False, null=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=False, null=False
    )
    publish = models.DateTimeField(
        default=datetime.strptime(
            str(datetime.today().date()), '%Y-%m-%d')
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
