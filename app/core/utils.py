"""
Util functions.
"""

from django.contrib.auth import get_user_model

from core.models import (
    User,
    Post,
)


def create_user(password: str = 'sample123', superuser: bool = False,
                **extra_fields) -> User:
    """Create and return user."""
    last_user = User.objects.last()
    new_user_id = 1 if not last_user else last_user.id + 1
    email = f'test{new_user_id}@example.com'

    user = get_user_model().objects.create_user(
        email=extra_fields.pop('email', email),
        password=password,
        **extra_fields
    )
    if superuser:
        """Promote to superuser."""
        get_user_model().objects.promote_to_superuser(user)

    return user


def create_post(body: str = 'Test body', **extra_fields) -> Post:
    """Create and return post."""
    last_post = Post.objects.last()
    title = 'Test title' if not last_post else last_post + '1'
    author = extra_fields.pop('author', create_user(superuser=True))

    if not isinstance(author, User):
        author = User.objects.get(pk=author)

    post = Post.objects.create(
        title=extra_fields.pop('title', title),
        body=body,
        author=author,
        **extra_fields
    )
    post.save()

    return post
