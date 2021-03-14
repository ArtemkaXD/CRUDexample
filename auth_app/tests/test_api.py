import json

from django.test import TestCase, Client
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from auth_app.models import User
from auth_app.serializers import UserSerializer

# initialize the APIClient and Faker
client = APIClient()
fake = Faker()


class GetUsersTest(TestCase):
    """ Test module for GET all and single users """

    def setUp(self):
        client.credentials()
        admin_profile = fake.simple_profile()
        self.admin = User.objects.create_superuser(
            username=admin_profile['username'], password=admin_profile['mail'],
            first_name=admin_profile['name'].partition(' ')[0],
            last_name=admin_profile['name'].partition(' ')[2]
        )
        for p in [fake.profile() for _ in range(5)]:
            User.objects.create_user(
                username=p['username'], password=p['mail'],
                first_name=p['name'].partition(' ')[0],
                last_name=p['name'].partition(' ')[2]
            )
        #create token for admin
        payload = {
            'username': admin_profile['username'],
            'password': admin_profile['mail']
        }
        response = client.post(
            reverse('auth_app:create_token'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        token = response.data
        client.credentials(HTTP_AUTHORIZATION='Token ' + token['token'])

    def test_get_all(self):
        response = client.get(reverse('auth_app:users-list'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_user(self):
        response = client.get(
            reverse('auth_app:users-detail', kwargs={'pk': self.admin.pk}))
        user = User.objects.get(pk=self.admin.pk)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        response = client.get(
            reverse('auth_app:users-detail', kwargs={'pk': 11}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateUsersTest(TestCase):
    """ Test module for create new users """

    def setUp(self):
        client.credentials()
        user_profile = fake.simple_profile()
        self.valid_payload = {
            'username': user_profile['username'],
            'password': user_profile['mail'],
            'first_name': user_profile['name'].partition(' ')[0],
            'last_name': user_profile['name'].partition(' ')[2]
        }

        self.invalid_payload = {
            'username': '',
            'password': user_profile['mail'],
            'first_name': user_profile['name'].partition(' ')[0],
            'last_name': user_profile['name'].partition(' ')[2]
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('auth_app:create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse('auth_app:create'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUsersTest(TestCase):
    """ Test module for UPDATE and DELETE users """

    def setUp(self):
        client.credentials()
        admin_profile = fake.simple_profile()
        self.admin = User.objects.create_superuser(
            username=admin_profile['username'], password=admin_profile['mail'],
            first_name=admin_profile['name'].partition(' ')[0],
            last_name=admin_profile['name'].partition(' ')[2]
        )

        user_profile = fake.simple_profile()
        self.user = User.objects.create_user(
            username=user_profile['username'], password=user_profile['mail'],
            first_name=user_profile['name'].partition(' ')[0],
            last_name=user_profile['name'].partition(' ')[2]
        )
        self.valid_payload = {
            'username': user_profile['username'],
            'password': user_profile['mail'],
            'first_name': 'Donald',
            'last_name': user_profile['name'].partition(' ')[2]
        }
        self.invalid_payload = {
            'username': '',
            'password': user_profile['mail'],
            'first_name': user_profile['name'].partition(' ')[0],
            'last_name': user_profile['name'].partition(' ')[2]
        }
        #create token for admin
        payload = {
            'username': admin_profile['username'],
            'password': admin_profile['mail']
        }
        response = client.post(
            reverse('auth_app:create_token'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        token = response.data
        client.credentials(HTTP_AUTHORIZATION='Token ' + token['token'])

    def test_valid_update_user(self):
        response = client.put(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        response = client.put(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_user(self):
        response = client.delete(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = client.delete(
            reverse('auth_app:users-detail', kwargs={'pk': 11}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PermissionsTest(TestCase):
    """ Test module for check users permissions """

    def setUp(self):
        client.credentials()
        admin_profile = fake.simple_profile()
        self.admin = User.objects.create_superuser(
            username=admin_profile['username'], password=admin_profile['mail'],
            first_name=admin_profile['name'].partition(' ')[0],
            last_name=admin_profile['name'].partition(' ')[2]
        )
        # create token for admin
        payload = {
            'username': admin_profile['username'],
            'password': admin_profile['mail']
        }
        response = client.post(
            reverse('auth_app:create_token'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.admin_token = response.data['token']

        user_profile = fake.simple_profile()
        self.user = User.objects.create_user(
            username=user_profile['username'], password=user_profile['mail'],
            first_name=user_profile['name'].partition(' ')[0],
            last_name=user_profile['name'].partition(' ')[2]
        )
        self.valid_payload = {
            'username': user_profile['username'],
            'password': user_profile['mail'],
            'first_name': 'Donald',
            'last_name': user_profile['name'].partition(' ')[2]
        }
        # create token for user
        payload = {
            'username': user_profile['username'],
            'password': user_profile['mail']
        }
        response = client.post(
            reverse('auth_app:create_token'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.user_token = response.data['token']

    def test_admin_update_permissions(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token)
        response = client.put(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_permissions(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = client.put(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_get_permissions(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token)
        response = client.get(
            reverse('auth_app:users-detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
