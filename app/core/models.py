"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractUser,
    PermissionsMixin,
)


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


class User(AbstractUser, PermissionsMixin):
    """Custom user in the system."""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
