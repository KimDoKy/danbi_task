from django.conf import settings
from django.db import models


class Routine(models.Model):
    ROUTINE_CATEGORY = [
        ('MIRACLE', '기상 관련'),
        ('HOMEWORK', '숙제 관련'),
    ]

    routine_id = models.AutoField(primary_key=True)
    account_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=10, choices=ROUTINE_CATEGORY)
    goal = models.CharField(max_length=5, null=True, blank=True)
    is_alarm = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_id.email

    def create_result(self):
        RoutineResult.objects.create(routine_id=self)

    def create_day(self, day):
        data = {
            'day': day,
            'routine_id': self
        }
        RoutineDay.objects.create(**data)


class RoutineResult(models.Model):
    NOT = 'NOT'
    TRY = 'TRY'
    DONE = 'DONE'
    RESULT = [
        (NOT, '안함'),
        (TRY, '시도'),
        (DONE, '완료'),
    ]
    routine_result_id = models.AutoField(primary_key=True)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    result = models.CharField(max_length=6, choices=RESULT, default=NOT)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.result


# 복합키 사용해야 함
class RoutineDay(models.Model):
    DAYS = [
        ('SUN', 'sun'),
        ('MON', 'mon'),
        ('TUE', 'tue'),
        ('WED', 'wed'),
        ('THU', 'thu'),
        ('FRI', 'fri'),
        ('SAT', 'sat')
    ]
    day = models.CharField(max_length=6, choices=DAYS)
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.routine_result_id
