import copy

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from .constants import *
from .models import Routine, RoutineResult
from .serializers import (
    RoutineSerializer,
    RoutineResultSerializer,
    RoutineDaySerializer,
)
from .utils import change_days_string, get_today_start_end


class RoutineView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoutineSerializer

    def post(self, request):
        result = dict()
        try:
            msg:str = API_MESSAGE_FAIL['CREATE']
            status:str = STATUS_FAIL['CREATE']

            data = copy.deepcopy(request.data)
            data['account_id'] = request.user.pk
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                routine_obj = serializer.save()
                routine_obj.create_result()
                days = request.data.getlist('days', None)
                if days:
                    routine_obj.create_days(days)
                data = {'routine_id': serializer.data['routine_id']}
                result['data'] = data

                msg = API_MESSAGE_OK['CREATE']
                status = STATUS_OK['CREATE']
        except Exception as e:
            msg = str(e)
        finally:
            message = {'msg': msg, 'status': status}
            result['message'] = message
        return Response(result)

    def put(self, request, routine_id):
        result = dict()
        try:
            data:dict =  {"routine_id": routine_id}
            status:str = STATUS_FAIL['UPDATE']

            routine_obj = get_object_or_404(Routine, routine_id=routine_id)
            if routine_obj:
                data = copy.deepcopy(request.data)
                data['account_id'] = request.user.pk
                serializer = self.serializer_class(routine_obj, data=data)
                if serializer.is_valid():
                    routine_obj = serializer.save()
                    days = request.data.getlist('days', None)
                    if days:
                        routine_id = routine_obj.days.first()
                        day_data = {
                            "routine_id": routine_id.pk,
                            "day": change_days_string(days)
                        }
                        routine_day_serializer = RoutineDaySerializer(
                            routine_obj.days.first(),
                            data=day_data
                        )
                        if routine_day_serializer.is_valid():
                            routine_day_serializer.save()

                            msg = API_MESSAGE_OK['UPDATE']
                            status = STATUS_OK['UPDATE']
                        else:
                            msg = routine_day_serializer.errors
                else:
                    msg = serializer.errors
        except Exception as e:
            msg = str(e)
        finally:
            message = {'msg': msg, 'status': status}
            result['message'] = message
            result['data'] = data
        return Response(result)

    def delete(self, request):
        result = dict()
        try:
            msg:str = API_MESSAGE_FAIL['DELETE']
            status:str = STATUS_FAIL['DELETE']

            account_id:int = request.data.get('account_id', None)
            routine_id:int = request.data.get('routine_id', None)

            data:dict = {"routine_id": routine_id}

            routine_obj = get_object_or_404(
                    Routine,
                    routine_id=routine_id,
                    account_id=account_id
                )
            if routine_obj:
                routine_obj.obj_delete()
                msg = API_MESSAGE_OK['DELETE']
                status = STATUS_OK['DELETE']
        except Exception as e:
            msg = str(e)
        finally:
            message = {"msg": msg, "status": status}
            result['message'] = message
            result['data'] = data
        return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def get_routine(request):
    result = dict()
    try:
        msg:str = API_MESSAGE_FAIL['DETAIL']
        status:str = STATUS_FAIL["DETAIL"]

        account_id:int = request.data.get('account_id', None)
        routine_id:int = request.data.get('routine_id', None)

        account_obj = get_object_or_404(User, id=account_id)
        routine_obj = get_object_or_404(
            Routine, 
            routine_id=routine_id,
            account_id=account_obj
        )

        if routine_obj:
            result_obj = routine_obj.results.first()
            data = {
                "goal": routine_obj.goal,
                "id": routine_obj.routine_id,
                "result": result_obj.result,
                "title": routine_obj.title
            }
            msg = API_MESSAGE_OK['DETAIL']
            status = STATUS_OK["DETAIL"]
            result['data'] = data
    except Exception as e:
        msg = str(e)
    finally:
        message = {"msg": msg, "status": status}
        result['message'] = message
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def get_routine_list(request):
    results = dict()
    try:
        msg:str = API_MESSAGE_FAIL["LIST"]
        status:str = STATUS_FAIL["LIST"]

        account_id:int = request.data.get('account_id', None)
        today:str = request.data.get('today', None)

        account_obj = get_object_or_404(User, id=account_id)
        today_start, today_end = get_today_start_end(today)
        routine_objs = Routine.objects.filter(
            account_id=account_id,
            created_at__range=[today_start, today_end]
        )

        routine_objs_info = list()
        for obj in routine_objs:
            result_obj = obj.results.first()
            result = {
                "goal": obj.goal,
                "id": obj.routine_id.__str__(),
                "result": result_obj.result,
                "title": obj.title
            }
            routine_objs_info.append(result)
        results['data'] = routine_objs_info

        msg = API_MESSAGE_OK["LIST"]
        status = STATUS_OK["LIST"]
    except Exception as e:
        msg = str(e)
    finally:
        message = {"msg": msg, "status": status}
        results['message'] = message
    return Response(results)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def update_after_routine(request):
    '''
    일정이 지난 후 진행한 할 일들에 대한 해결 여부 기록
    input
    {
        routine_id: int,
        result: str(NOT, TRY, DONE)
    }
    output
    {
        data:
            routine_result_id: int
            result: str(NOT, TRY, DONE)
        message:
            msg: str,
            status: str
    }
    '''
    results = dict()
    try:
        msg:str = API_MESSAGE_FAIL["RESULT_UPDATE"]
        status:str = STATUS_FAIL["RESULT_UPDATE"]

        routine_id:int = request.data.get('routine_id', None)
        result:str = request.data.get('result', None)

        routine_obj = get_object_or_404(
            Routine,
            routine_id=routine_id
        )
        result_obj = routine_obj.results.first()
        data = {'result': result}
        serializer = RoutineResultSerializer(result_obj, data=data)
        if serializer.is_valid():
            result_obj = serializer.save()
            data = {
                "routine_result_id": result_obj.routine_result_id,
                "result": result_obj.result
            }
            results['data'] = data

            msg = API_MESSAGE_OK["RESULT_UPDATE"]
            status = STATUS_OK["RESULT_UPDATE"]
        else:
            msg = serializer.errors
    except Exception as e:
        msg = str(e)
    finally:
        message = {"msg": msg, "status": status}
        results['message'] = message
    return Response(results)
