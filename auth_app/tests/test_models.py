from django.test import TestCase
from CRUDexample.settings import AUTH_USER_MODEL, INSTALLED_APPS

from auth_app.models import User


class SettingsTest(TestCase):
    def test_account_is_configured(self):
        self.assertTrue('auth_app.apps.AuthAppConfig' in INSTALLED_APPS)
        self.assertTrue('auth_app.User' == AUTH_USER_MODEL)


class UserManagerTest(TestCase):

    def setUp(self):
        self.worker = User.objects.create_user(
            username='Worker', password='notgod')
        self.boss = User.objects.create_superuser(
            username='Boss', password='god')

    def test_user_create(self):
        user = self.worker
        self.assertEqual(user.username, 'Worker')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_superuser_create(self):
        user = self.boss
        self.assertEqual(user.username, 'Boss')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

