"""
URL mappings for the blog API.
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from . import views

VIEWSETS = [
    ('posts', views.BlogViewSet),
]

router = DefaultRouter()
for name, viewset in VIEWSETS:
    router.register(name, viewset)

app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
