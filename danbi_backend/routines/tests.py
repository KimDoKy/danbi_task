import random
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import RoutineResult, RoutineDay, Routine
from .views import STATUS_OK, STATUS_FAIL


class RouineTest(TestCase):
    def setUp(self):
        self.user_data = {'email': 'test@wink.com', 'password': 'danbi1234!@#$'}

        self.client = APIClient()

        self.routine_url = reverse('routines:routine')
        self.routine_target_url = reverse('routines:target')
        self.routine_list_url = reverse('routines:list')

        self.create_user()
        self.cerate_test_routine()

    def create_user(self):
        get_user_model().objects.create_user(**self.user_data)

    def get_token(self):
        res = self.client.post('/login/', self.user_data)
        token = 'jwt ' + res.data.get('token', None)
        return token

    def cerate_test_routine(self):
        self.get_token()
        titles = [f"title{i}" for i in range(10)]
        for title in titles:
            data = {
                "account_id": get_user_model().objects.first(),
                "title": title,
                "category": random.choice(Routine.ROUTINE_CATEGORY),
                "goal": "",
                "is_alarm": True
            }
            obj = Routine.objects.create(**data)
            obj.create_result()
            days = random.choices(RoutineDay.DAYS, k=random.randint(1,7))
            for day in days:
                obj.create_day(day)

    def test_create_routine(self):
        token = self.get_token()
        data = {
            "title": " ",
            "category": "HOMEWORK",
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        res = self.client.post(
            self.routine_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message']['status'], STATUS_OK['CREATE'])

    def test_routine_target_check(self):
        token = self.get_token()
        data = {
            "account_id": 1,
            "routine_id": 3
        }
        res = self.client.post(
            self.routine_target_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['data']['id'], data['routine_id'])
        self.assertEqual(res.data['message']['status'], STATUS_OK['DETAIL'])

    '''
    def test_modify_routine(self):
        token = self.get_token()
        data = {}

        url = self.check_list_url + '/' + routine_id
        res = self.client.put(
            url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual()

    def test_delete_routine(self):
        token = self.get_token()
        data = {}
        res = self.client.delete(
            self.routine_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual()

    def test_routine_check_list(self):
        token = self.get_token()
        data = {}
        res = self.client.get(
            self.routine_list_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual()
    '''
