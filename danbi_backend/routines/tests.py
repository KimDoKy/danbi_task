import random
import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import RoutineResult, RoutineDay, Routine
from .utils import change_days_string
from .views import STATUS_OK


class RouineTest(TestCase):
    def setUp(self):
        self.user_data = {'email': 'test@wink.com', 'password': 'danbi1234!@#$'}
        self.days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

        self.client = APIClient()

        self.routine_url = reverse('routines:routine')
        self.routine_target_url = reverse('routines:target')
        self.routine_list_url = reverse('routines:list')
        self.update_result_url = reverse('routines:update-result')

        self.create_user()
        self.create_test_routine()

    def create_user(self):
        get_user_model().objects.create_user(**self.user_data)

    def get_token(self):
        res = self.client.post('/login/', self.user_data)
        token = 'jwt ' + res.data.get('token', None)
        return token

    def create_test_routine(self):
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
            days = random.sample(self.days, k=random.randint(1,7))
            days = change_days_string(days)
            obj.create_days(days)

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

    def test_modify_routine(self):
        token = self.get_token()
        routine_obj = Routine.objects.first()

        data = {
            "title": "update title",
            "category": Routine.ROUTINE_CATEGORY[0][0],
            "goal": "",
            "is_alarm": True,
            "days": ["MON", "SUN"]
        }
        url = f"{self.routine_url}{routine_obj.routine_id}/"
        res = self.client.put(
            url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        modified_routine_obj = Routine.objects.first()
        modified_day_obj = routine_obj.days.first()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message']['status'], STATUS_OK['UPDATE'])
        self.assertEqual(routine_obj.routine_id, modified_routine_obj.routine_id)
        self.assertNotEqual(routine_obj.title, modified_routine_obj.title)
        self.assertEqual(modified_day_obj.day, change_days_string(data['days']))

    def test_delete_routine(self):
        token = self.get_token()
        routine_obj = get_object_or_404(Routine, routine_id=1)
        result_obj = routine_obj.results.first()

        data = {
            "routine_id": 1,
            "account_id": 1
        }
        res = self.client.delete(
            self.routine_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message']['status'], STATUS_OK['DELETE'])
        is_obj = Routine.objects.filter(routine_id=1).first()
        self.assertFalse(is_obj)
        is_result_obj = get_object_or_404(
            RoutineResult,
            routine_result_id=result_obj.routine_result_id
        )
        self.assertNotEqual(result_obj.is_deleted, is_result_obj.is_deleted)
        self.assertNotEqual(result_obj.routine_id, is_result_obj.routine_id)

    def test_routine_check_list(self):
        token = self.get_token()
        today = datetime.datetime.now().date()
        data = {
            "account_id": 1,
            "today": today
        }
        res = self.client.post(
            self.routine_list_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message']['status'], STATUS_OK['LIST'])

    def test_routine_update_result(self):
        routine_obj = get_object_or_404(
            Routine,
            routine_id=1
        )
        result_obj = routine_obj.results.first()

        token = self.get_token()
        data = {
            "account_id": 1,
            "routine_id": 1,
            "result": "DONE"
        }
        res = self.client.post(
            self.update_result_url,
            data=data,
            HTTP_AUTHORIZATION=token,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['message']['status'], STATUS_OK['RESULT_UPDATE'])

        new_result_obj = routine_obj.results.first()
        self.assertNotEqual(result_obj.result, new_result_obj.result)
