"""
Util functions.
"""

from core.models import User


def create_user(email: str = 'test@example.com', username: str = 'TestUser',
                password: str = 'sample123', superuser: bool = False) -> User:
    """Create and return user."""
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
    )
    if superuser:
        """Promote to superuser."""
        User.objects.promote_to_superuser(user)

    return user
