"""
Django admin customizations.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import (
    User,
    Post,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['username', 'email']
    list_filter = ['username', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    """Define the admin pages for posts."""
    ordering = ['id']
    list_display = ['title', 'author', 'status']
    list_filter = ['author', 'status', 'created', 'updated', 'publish']
    fieldsets = (
        (None, {'fields': ('title', 'author', 'status', 'body')}),
        (_('Important dates'), {'fields': ('created', 'publish', 'updated')})
    )
    readonly_fields = ['created', 'publish', 'updated']
