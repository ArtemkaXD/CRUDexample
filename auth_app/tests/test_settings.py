from auth_app.models import User
from django.test import TestCase
from CRUDexample.settings import AUTH_USER_MODEL, INSTALLED_APPS


class SettingsTest(TestCase):
    def test_account_is_configured(self):
        self.assertTrue('auth_app.apps.AuthAppConfig' in INSTALLED_APPS)
        self.assertTrue('auth_app.User' == AUTH_USER_MODEL)