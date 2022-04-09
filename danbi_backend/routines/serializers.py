from rest_framework import serializers
from .models import Routine, RoutineResult, RoutineDay


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ('__all__')


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ('__all__')


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ('__all__')

