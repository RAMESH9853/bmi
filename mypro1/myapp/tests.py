from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Profile


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_profile(self):
        url = reverse('profile-list-create')
        data = {
            'full_name': 'John Doe',
            'gender': 'Male',
            'height': '180.00',
            'weight': '80.00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.objects.get().full_name, 'John Doe')

    def test_get_profile(self):
        url = reverse('profile-retrieve-update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['full_name'], self.user.profile.full_name)

    def test_update_profile(self):
        url = reverse('profile-retrieve-update')
        data = {
            'full_name': 'Jane Doe',
            'gender': 'Female',
            'height': '170.00',
            'weight': '60.00'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.get().full_name, 'Jane Doe')




from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth.models import User


class ProfileTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.profile_data = {'full_name': 'John Doe', 'gender': 'M', 'height': 175, 'weight': 75, 'bmi': 24.49, 'user': self.user.id}
        self.response = self.client.post(reverse('profile-list'), self.profile_data, format='json')

    def test_create_profile(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_profile_list(self):
        response = self.client.get(reverse('profile-list'))
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_detail(self):
        profile = Profile.objects.first()
        response = self.client.get(reverse('profile-detail', kwargs={'pk': profile.id}))
        serializer = ProfileSerializer(profile)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        profile = Profile.objects.first()
        updated_profile_data = {'full_name': 'Jane Doe', 'gender': 'F', 'height': 160, 'weight': 60, 'bmi': 23.44, 'user': self.user.id}
        response = self.client.put(reverse('profile-detail', kwargs={'pk': profile.id}), updated_profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_profile(self):
        profile = Profile.objects.first()
        response = self.client.delete(reverse('profile-detail', kwargs={'pk': profile.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
