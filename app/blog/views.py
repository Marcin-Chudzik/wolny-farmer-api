"""
Views for the blog API.
"""
from core.models import Post
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from . import serializers


class BlogViewSet(viewsets.ModelViewSet):
    """View for manage blog API."""
    serializer_class = serializers.PostSerializer
    queryset = Post.published.all()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.PostSerializer
        elif self.action == 'detail':
            return serializers.PostDetailSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        """Create a new post."""
        if not self.request.user.is_superuser:
            raise PermissionDenied('Only admins are allowed to create a posts')
        serializer.save(author=self.request.user)
