"""
Test for the Django admin modifications.
"""
from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse
from django.contrib import admin

from core.utils import (
    create_user,
    create_post,
)


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        self.client = Client()
        self.admin_user = create_user(superuser=True)
        self.client.force_login(self.admin_user)
        self.user = create_user(email='other@example.com')
        self.post = create_post(author=self.user.id)

    def test_admin_models_patterns(self):
        """
        Test all default url patterns in admin site for each registered model.

        Tested url patterns:
        - core_<model>_changelist
        - core_<model>_add
        - core_<model>_history
        - core_<model>_delete
        - core_<model>_change
        """
        admin_models = [model for model in admin.site._registry.values() if 'core' in str(model)]

        for model in admin_models:
            for pattern in model.get_urls():
                if pattern.name is not None:
                    model_name = str(model.opts).replace('core.', '')
                    model_instance = getattr(self, model_name)
                    pattern_params = [
                        'id' if 'id' in param else param
                        for param in pattern.pattern.converters
                    ]

                    url_params = [getattr(model_instance, param) for param in pattern_params]

                    if len(url_params) > 0:
                        url = reverse(f"admin:{pattern.name}", args=url_params)
                    else:
                        url = reverse(f"admin:{pattern.name}")

                    res = self.client.get(url)

                    if 'list' in pattern.name:
                        for field in model.list_display:
                            self.assertContains(res, getattr(model_instance, field))

                    self.assertEqual(res.status_code, 200)

    """ADMIN USER TESTS"""
    def test_auth_user_password_change(self):
        """Test the authenticated user password change page works."""
        url = reverse('admin:auth_user_password_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
