"""
Util functions.
"""

from django.contrib.auth import get_user_model


def create_user(email: str = 'test@example.com', password: str = 'sample123',
                superuser: bool = False, **extra_fields) -> "User":
    """Create and return user."""
    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        **extra_fields,
    )
    if superuser:
        """Promote to superuser."""
        get_user_model().objects.promote_to_superuser(user)

    return user
