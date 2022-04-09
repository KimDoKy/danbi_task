from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient


class UserTest(TestCase):
    def setUp(self):
        self.email = "test@wink.com"
        self.password = "danbiback3#"

        self.client = APIClient()
        self.user_model = get_user_model()

        self.registration_url = reverse('accounts:registration')
        self.login_url = '/login/'
        self.logout_url = reverse('accounts:logout')

    def test_registration(self):
        old_cnt = self.user_model.objects.count()

        data = {'email': self.email, 'password': self.password}
        res = self.client.post(self.registration_url, data)

        new_cnt = self.user_model.objects.count()

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(old_cnt, new_cnt)

        self.assertTrue(res.data['result'])

    def test_registration_invalid_email(self):
        old_cnt = self.user_model.objects.count()

        failed_email = 'tester'
        data = {'email': failed_email, 'password': self.password}
        res = self.client.post(self.registration_url, data)

        new_cnt = self.user_model.objects.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(old_cnt, new_cnt)
        self.assertFalse(res.data['result'])

    def test_registration_invalid_password1(self):
        old_cnt = self.user_model.objects.count()

        failed_pw_1 = "asdf&*1"
        data = {'email': self.email, 'password': failed_pw_1}
        res = self.client.post(self.registration_url, data)

        new_cnt = self.user_model.objects.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(old_cnt, new_cnt)
        self.assertFalse(res.data['result'])

    def test_registration_invalid_password2(self):
        old_cnt = self.user_model.objects.count()

        failed_pw_2 = "asdf1234"
        data = {'email': self.email, 'password': failed_pw_2}
        res = self.client.post(self.registration_url, data)

        new_cnt = self.user_model.objects.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(old_cnt, new_cnt)
        self.assertFalse(res.data['result'])

    def test_registration_invalid_password3(self):
        old_cnt = self.user_model.objects.count()

        failed_pw_3 = "asdf!@#$"
        data = {'email': self.email, 'password': failed_pw_3}
        res = self.client.post(self.registration_url, data)

        new_cnt = self.user_model.objects.count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(old_cnt, new_cnt)
        self.assertFalse(res.data['result'])

    def signup_user(self):
        data = {'email': self.email, 'password': self.password}
        user = self.user_model.objects.create_user(**data)
        return user

    def test_login(self):
        user = self.signup_user()

        data = {'email': 'fade@email.com', 'password': self.password}
        res = self.client.post(self.login_url, data)
        self.assertNotEqual(res.status_code, 200)

        data = {'email': self.email, 'password': self.password}
        res = self.client.post(self.login_url, data)
        self.assertEqual(res.status_code, 200)

    def test_logout(self):
        user = self.signup_user()
        data = {'email': self.email, 'password': self.password}
        res = self.client.post(self.login_url, data)
        token = 'jwt ' + res.data.get('token', None)

        res = self.client.post(
            self.logout_url, 
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['result'])
