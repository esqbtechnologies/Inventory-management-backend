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
from ..models.Verificationmodels import verification
from ..models.Assetmodels import asset

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
        return JsonResponse({'error': 'user is not authorized to start session'}, status=status.HTTP_400_BAD_REQUEST)


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
                delsession = session.objects.get(sessionId=id,isActive=True)
                delsession.sessionEndDate = datetime.now()
                delsession.isActive = False
                all_assets = asset.objects.filter(is_deleted = False)
                unvarified_asset = []
                for datas in all_assets:
                    if verification.objects.filter(sessionId=id).filter(asset=datas).exists():
                        if verification.objects.filter(sessionId=id).filter(asset=datas).filter(flag=True).exists():
                            continue
                        else:
                            data = serializers.serialize('json', [datas,])
                            struct = json.loads(data)
                            data = json.dumps(struct[0])
                            unvarified_asset.append(data)
                    else:
                        print(datas)
                        dummyver = verification()
                        dummyver.date = date.today()
                        dummyver.sessionId = id
                        dummyver.asset = datas
                        dummyver.flag = False
                        dummyver.save()
                        data = serializers.serialize('json', [datas,])
                        struct = json.loads(data)
                        data = json.dumps(struct[0])
                        unvarified_asset.append(data)    
                delsession.save()        
                return JsonResponse(unvarified_asset, safe = False,status=status.HTTP_200_OK)
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


class get_all_session(APIView):

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
                all_session = session.objects.all()
                response_data = []
                for sessions in all_session:
                    data = serializers.serialize('json', [sessions,])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    response_data.append(data)
                return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
            except:
                return JsonResponse({'error': 'No sessions exists to show'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not authorized to get all Session'}, status=status.HTTP_400_BAD_REQUEST)
    
class last_session_data(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self,request):
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
                    response_data = []
                    sdata = Verification.objects.filter(sessionId=sess.sessionId)
                    for sdatas in sdata:
                        code = sdatas.asset.item_code
                        name = sdatas.asset.item_name
                        is_deleted = sdatas.asset.is_deleted
                        data = serializers.serialize('json', [sdatas,])
                        struct = json.loads(data)
                        data = json.dumps(struct[0])
                        data = json.loads(data)
                        data['fields']['item_code'] = code
                        data['fields']['item_name'] = name
                        data['fields']['is_deleted'] = is_deleted
                        response_data.append(data)
                    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
                except:
                    return JsonResponse({'Result': 'No Session exists to Send data'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not authorized to Restart session'}, status=status.HTTP_400_BAD_REQUEST)
    
