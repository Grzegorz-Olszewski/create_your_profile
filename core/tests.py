from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Profile
from core.forms import ProfileForm


class ProfileTest(TestCase):

    def create_user_with_profile(self):
        user = User.objects.create_user('Tom', 'test@example.com', 'iwonttellyou')
        Profile.objects.create(
            user=user,
            past_address="Wyścigowa 56g/2a, Wroclaw, Poland",
            present_address="Coal Drops Yard, London, United Kingdom",
            phone_number="123456789"
        )
        return user

    def test_user_creation(self):
        user = self.create_user_with_profile()
        self.assertTrue(isinstance(user.profile, Profile))
        self.assertEqual(user.profile.past_address, "Wyścigowa 56g/2a, Wroclaw, Poland")
        self.assertEqual(user.profile.phone_number, "123456789")

    def test_login(self):
        client = Client()
        response = client.post(reverse('login'),
                               {'username': 'Tom', 'password': 'iwonttellyou'})
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        client = Client()
        client.post(reverse('login'), {'username': 'Tom', 'password': 'iwonttellyou'})
        response = client.post(reverse('logout'), follow=True)
        self.assertContains(response, "Logged out")

    def test_details(self):
        self.create_user_with_profile()
        client = Client()
        client.post(reverse('login'), {'username': 'Tom', 'password': 'iwonttellyou'})
        response = client.get(reverse('details'), follow=True)
        self.assertContains(response, "Coal Drops Yard")

    def test_cant_get_to_detail_when_not_logged_in(self):
        client = Client()
        response = client.get(reverse('details'))
        self.assertEqual(response.status_code, 302)

    def test_delete(self):
        self.create_user_with_profile()
        client = Client()
        client.post(reverse('login'), {'username': 'Tom', 'password': 'iwonttellyou'})
        response = client.get(reverse('delete'), follow=True)
        self.assertContains(response, 'Are you sure you want to delete your profile?')
        response = client.post(reverse('delete'), follow=True)
        self.assertEqual(hasattr(response.wsgi_request.user, "profile"), False)

    def test_update_profile(self):
        self.create_user_with_profile()
        client = Client()
        client.post(reverse('login'), {'username': 'Tom', 'password': 'iwonttellyou'})
        data = {"past_address": "Tomstreet 13",
                "present_address": "Adamstreet 14",
                "phone_number": "42141242"}
        response = client.post(reverse('update_profile'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        response = client.get(reverse('details'), follow=True)
        self.assertContains(response, "Tomstreet 13")
        self.assertEqual(response.wsgi_request.user.profile.phone_number, "42141242")

    def test_cant_get_to_update_profile_when_not_logged_in(self):
        client = Client()
        response = client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 302)

    def test_cant_get_to_delete_when_not_logged_in(self):
        client = Client()
        response = client.get(reverse('delete'))
        self.assertEqual(response.status_code, 302)

    def test_valid_profile_form(self):
        user = self.create_user_with_profile()
        data = {"past_address": user.profile.past_address,
                "present_address": user.profile.present_address,
                "phone_number": user.profile.phone_number}
        form = ProfileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_profile_form(self):
        user = self.create_user_with_profile()
        data = {"past_address": user.profile.past_address,
                "present_address": user.profile.present_address,
                "phone_number": ""}
        form = ProfileForm(data=data)
        self.assertFalse(form.is_valid())
