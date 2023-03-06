from django.http import JsonResponse
from requests import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import jwt
import ivnt_mngmnt.settings as set
from ..models.Usermodels import User
from ..models.Sessionmodels import session
from datetime import date
from datetime import datetime
import uuid
from rest_framework import status
import json
from django.core import serializers


class create_session(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            id = uuid.uuid4()
            newsession = session()
            newsession.isActive = True
            newsession.sessionStartDate = date.today()
            newsession.sessionId = id.hex
            newsession.save()
            data = serializers.serialize('json', [newsession,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        return Response({'error': 'user is not authorized to start session'}, status=status.HTTP_400_BAD_REQUEST)


class end_session(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            id = request.data['sessionId']
            try:
                delsession = session.objects.get(sessionId=id)
                delsession.sessionEndDate = datetime.now()
                delsession.isActive = False
                delsession.save()
                return JsonResponse({'Result': 'session deleted Succesfully'}, status=status.HTTP_200_OK)
            except:
                return JsonResponse({'error': 'No such session exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'user is not authorized to end session'}, status=status.HTTP_400_BAD_REQUEST)


class get_active_session(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        try:
            activesession = session.objects.get(isActive=True)
            data = serializers.serialize('json', [activesession,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        except:
            return JsonResponse({'Result': 'No Active Session exists'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
# API To restart latest session
class restart_last_session(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            try:
                activesession = session.objects.get(isActive=True)
                return JsonResponse({'Result': 'There exits an already active session'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except:
                try:
                    data = session.objects.all().order_by('-sessionEndDate')
                    sess = data[0]
                    sess.isActive = True
                    sess.sessionEndDate = None
                    sess.save()
                    data = serializers.serialize('json', [sess,])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
                except:
                    return JsonResponse({'Result': 'No Session exists to Restart'}, status=status.HTTP_204_NO_CONTENT)

        return JsonResponse({'error': 'user is not authorized to Restart session'}, status=status.HTTP_400_BAD_REQUEST)        
