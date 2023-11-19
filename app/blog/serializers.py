"""
Serializers for blog API.
"""
from core.models import (
    Post,
    User,
)
from core.utils import create_post
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    """Serializer for posts."""

    class Meta:
        model = Post
        fields = ['id', 'title', 'body']
        read_only_fields = ['id']
        extra_kwargs = {
            'author': {'write_only': True},
            'title': {'min_length': 5},
            'body': {'min_length': 30},
        }

    def create(self, validated_data: dict[str, str or User]) -> Post:
        """Create and return new post."""
        return create_post(**validated_data)

    def update(self, instance, validated_data: dict[str, str or User]) -> Post:
        """Update and return post."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class PostDetailSerializer(PostSerializer):
    """Serializer for the post detail view."""

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields
