import copy

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
from .utils import change_days_string


class RoutineView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        result = dict()
        try:
            data = copy.deepcopy(request.data)
            data['account_id'] = request.user.pk
            serializer = RoutineSerializer(data=data)
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
            else:
                msg = API_MESSAGE_FAIL['CREATE']
                status = STATUS_FAIL['CREATE']
        except Exception as e:
            msg = str(e)
            status = STATUS_FAIL['CREATE']
        finally:
            message = {'msg': msg, 'status': status}
            result['message'] = message
        return Response(result)

    def put(self, request, routine_id):
        result = dict()
        try:
            data =  {"routine_id": routine_id}
            result['data'] = data

            routine_obj = Routine.objects.filter(routine_id=routine_id).first()
            if routine_obj:
                data = copy.deepcopy(request.data)
                data['account_id'] = request.user.pk
                serializer = RoutineSerializer(routine_obj, data=data)
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
                            status = STATUS_FAIL['UPDATE']
                else:
                    msg = serializer.errors
                    status = STATUS_FAIL['UPDATE']
        except Exception as e:
            msg = str(e)
            status = STATUS_FAIL['UPDATE']
        finally:
            message = {'msg': msg, 'status': status}
            result['message'] = message
        return Response(result)

    def delete(self, request):
        result = dict()
        try:
            account_id = request.data.get('account_id', None)
            routine_id = request.data.get('routine_id', None)

            data = {"routine_id": routine_id}
            result['data'] = data

            routine_obj = Routine.objects.filter(
                    routine_id=routine_id,
                    account_id=account_id
                ).first()
            if routine_obj:
                routine_obj.delete()
                msg = API_MESSAGE_OK['DELETE']
                status = STATUS_OK['DELETE']
        except Exception as e:
            msg = str(e)
            status = STATUS_FAIL['DELETE']
        finally:
            message = {"msg": msg, "status": status}
            result['message'] = message
        return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def get_routine(request):
    try:
        result = dict()

        msg = API_MESSAGE_FAIL['DETAIL']
        status = STATUS_FAIL["DETAIL"]

        account_id = request.data.get('account_id', None)
        routine_id = request.data.get('routine_id', None)

        account_obj = User.objects.filter(id=account_id).first()
        routine_obj = Routine.objects.filter(
                routine_id=routine_id,
                account_id=account_obj
            ).first()

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
        msg = API_MESSAGE_FAIL["LIST"]
        status = STATUS_FAIL["LIST"]

        account_id = request.data.get('account_id', None)
        today = request.data.get('today', None)

        account_obj = User.objects.filter(id=account_id).first()
        routine_objs = Routine.objects.filter(
            account_id=account_id,
            created_at__range=[f"{today} 00:00:00", f"{today} 23:59:59"]
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
        msg = e
        status = STATUS_FAIL['LIST']
    finally:
        message = {"msg": msg, "status": status}
        results['message'] = message
    return Response(results)
