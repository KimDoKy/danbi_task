import copy

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from .models import Routine, RoutineResult
from .serializers import (
    RoutineSerializer,
    RoutineResultSerializer,
    RoutineDaySerializer,
)
from .utils import change_days_string


STATUS_OK = {
    "CREATE": "ROUTINE_CREATE_OK",
    "LIST": "ROUTINE_LIST_OK",
    "DETAIL": "ROUTINE_DETAIL_OK",
    "UPDATE": "ROUTINE_UPDATE_OK",
    "DELETE": "ROUTINE_DELETE_OK",
}
STATUS_FAIL = {
    "CREATE": "ROUTINE_CREATE_FAIL",
    "LIST": "ROUTINE_LIST_FAIL",
    "DETAIL": "ROUTINE_DETAIL_FAIL",
    "UPDATE": "ROUTINE_UPDATE_FAIL",
    "DELETE": "ROUTINE_DELETE_FAIL",
}


class RoutineView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            result = dict()
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
                message = {
                    'msg': 'Routine이 생성되었습니다.',
                    'status': STATUS_OK['CREATE']
                }
                result['message'] = message
            else:
                message = {
                    'msg': 'Routine 생성이 실패하였습니다.',
                    'status': STATUS_FAIL['CREATE']
                }
                result['message'] = message

        except Exception as e:
            message = {
                'msg': e,
                'status': STATUS_FAIL['CREATE']
            }
            result['message'] = message
        return Response(result)

    def put(self, request, routine_id):
        try:
            result = {
                "data": {
                    "routine_id": routine_id
                }
            }
            routine_obj = Routine.objects.filter(routine_id=routine_id).first()
            if routine_obj:
                data = copy.deepcopy(request.data)
                data['account_id'] = request.user.pk
                serializer = RoutineSerializer(routine_obj, data=data)
                if serializer.is_valid():
                    routine_obj = serializer.save()
                    days = request.data.getlist('days', None)
                    if days:
                        routine_id = routine_obj.routineday_set.first()
                        data = {
                            "routine_id": routine_id.pk,
                            "day": change_days_string(days)
                        }
                        routine_day_serializer = RoutineDaySerializer(routine_obj.routineday_set.first(), data=data)
                        if routine_day_serializer.is_valid():
                            routine_day_serializer.save()
                        else:
                            print(routine_day_serializer.errors)
                    message = {
                        'msg': '',
                        'status': STATUS_OK['UPDATE']
                    }
                    result['message'] = message
                else:
                    message = {
                        'msg': serializer.errors,
                        'status': STATUS_FAIL['UPDATE']
                    }
                    result['message'] = message
        except Exception as e:
            message = {
                'msg': e,
                'status': STATUS_FAIL['UPDATE']
            }
            result['message'] = message
        return Response(result)

    def delete(self, request):
        '''
        # Routine 삭제
        input
        {
            account_id: int,
            routine_id: int
        }

        output
        {
            data: dict{
                routine_id: int
            },
            message: dict{
                msg: str,
                status: str("ROUTINE_DELETE_OK")
            }
        }
        '''
        try:
            ...
        except Exception as e:
            ...
        return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def get_routine(request):
    # Routine 단건 조회
    try:
        message = {
            "msg": "조회 실패",
            "status": STATUS_FAIL["DETAIL"]
        }
        result = {'message': message}
        account_id = request.data.get('account_id', None)
        routine_id = request.data.get('routine_id', None)

        account_obj = User.objects.filter(id=account_id).first()
        routine_obj = Routine.objects.filter(
            routine_id=routine_id,
            account_id=account_obj
        ).first()
        if routine_obj:
            result_obj = routine_obj.routineresult_set.first()
            data = {
                "goal": routine_obj.goal,
                "id": routine_obj.routine_id,
                "result": result_obj.result,
                "title": routine_obj.title
            }
            message = {
                "msg": "조회 성공",
                "status": STATUS_OK["DETAIL"]
            }
            result['data'] = data
            result['message'] = message
    except Exception as e:
        message['msg'] = e
        result['message'] = message
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def get_routine_list(request):
    '''
    # Routine 목록 조회
    input
    {
        account_id: int,
        today: date(yyyy-mm-dd)
    }

    output
    {
        data: list[
            dict{
                goal: str("     2 "),
                id: int,
                result: str("NOT"),
                title: str
            }...
        ],
        message: dict{
            msg: str,
            status: str("ROUTINE_LIST_OK")
        }
    }
    '''
    try:
        ...
    except Exception as e:
        message = {
            'msg': e,
            'status': STATUS_FAIL['CREATE']
        }
        result['message'] = message
    return Response(result)
