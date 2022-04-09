import sys
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import LogoutToken
from .serializers import LogoutTokenSerializer, UserSerializer
from .validators import CustomPasswordValidator

class RegistrationView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        result = {'result': False}
        try:
            email = request.data.get('email', None)
            password = request.data.get('password', None)

            validator = CustomPasswordValidator()
            validator.validate(password)

            data = {'email': email, 'password': password}
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                result['result'] = True
            else:
                result['message'] = serializer.errors
        except Exception as e:
            result['message'] = e.message
        return Response(result)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        result = {'result': False}
        try:
            old_token = LogoutToken.objects.filter(user=request.user).first()
            if old_token:
                old_token.delete()
            token = request.auth.decode('utf-8')
            data = {
                'user': request.user.pk,
                'token': token
            }
            serializer = LogoutTokenSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                result['result'] = True
            else:
                result['message'] = serializer.errors
        except Exception as e:
            result['message'] = e
        return Response(result)
