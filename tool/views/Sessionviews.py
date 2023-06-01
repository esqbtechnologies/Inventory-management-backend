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
from ..models.Locationmodels import location
from rest_framework.pagination import PageNumberPagination

class create_session(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            if location.objects.filter(lname = request.data['location']).exists():
                if session.objects.filter(isActive=True).filter(location__lname = request.data['location']).exists():
                    return JsonResponse({'Response':'An active session already exists for the location'})
                id = uuid.uuid4()
                if session.objects.filter(location__lname=request.data['location']).filter(is_latest=True).exists():
                    session.objects.filter(location__lname=request.data['location'],is_latest = True).update(is_latest= False)
                newsession = session()
                newsession.isActive = True
                newsession.sessionStartDate = date.today()
                newsession.sessionId = id.hex
                newsession.location = location.objects.get(lname = request.data['location'])
                newsession.save()
                data = serializers.serialize('json', [newsession,])
                struct = json.loads(data)
                data = json.dumps(struct[0])
                data = json.loads(data)
                data['fields']['locationName'] = request.data['location'] 
                data = json.dumps(data)
                return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse({'error':'The location you requested for to start session dos not exists in the Db.'},status = status.HTTP_204_NO_CONTENT)    
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
                        if datas.Warehouse_location == delsession.location:
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
                        else:
                            continue    
                delsession.save()        
                return JsonResponse(unvarified_asset, safe = False,status=status.HTTP_200_OK)
            except:
                return JsonResponse({'error': 'No such session exists'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'user is not authorized to end session'}, status=status.HTTP_400_BAD_REQUEST)


class get_active_session(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        try:
            activesession = session.objects.get(isActive=True,location__lname = request.data['location'])
            data = serializers.serialize('json', [activesession,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            data = json.loads(data)
            data['fields']['location_name'] = request.data['location'] 
            data = json.dumps(data)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        except:
            is_active = False
            return JsonResponse(is_active,safe = False, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

# API To restart latest session


class restart_last_session(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            try:
                activesession = session.objects.get(isActive=True,location__lname = request.data['location'])
                return JsonResponse({'Result': 'There exits an already active session in this location'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except:
                try:
                    data = session.objects.filter(location__lname = request.data['location'],is_latest=True)
                    sess = data[0]
                    sess.isActive = True
                    sess.sessionEndDate = None
                    sess.save()
                    data = serializers.serialize('json', [sess,])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    data = json.loads(data)
                    data['fields']['location_name'] = request.data['location']
                    data = json.dumps(data)
                    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
                except:
                    return JsonResponse({'Result': 'No Session exists to Restart'}, status=status.HTTP_204_NO_CONTENT)

        return JsonResponse({'error': 'user is not authorized to Restart session'}, status=status.HTTP_400_BAD_REQUEST)


class get_all_session(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            try:
                all_session = session.objects.filter(location__lname = request.data['location'])
                response_data = []
                for sessions in all_session:
                    data = serializers.serialize('json', [sessions,])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    data = json.loads(data)
                    data['fields']['location_name'] = request.data['location']
                    data = json.dumps(data)
                    response_data.append(data)
                return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
            except:
                return JsonResponse({'error': 'No sessions exists to show'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not authorized to get all Session'}, status=status.HTTP_400_BAD_REQUEST)
    
class last_session_data(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            try:
                activesession = session.objects.get(isActive=True,location__lname = request.data['location'])
                return JsonResponse({'Result': 'There exits an already active session'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except:
                try:
                    data = session.objects.filter(location__lname = request.data['location'],is_latest=True)
                    sess = data[0]
                    response_data = []
                    page_size = 100
                    paginator = PageNumberPagination()
                    paginator.page_size = page_size
                    aset = verification.objects.filter(sessionId=sess.sessionId)
#                     aset = verification.objects.filter(sessionId=sess.sessionId).order_by("item_code")
                    sdata = paginator.paginate_queryset(aset,request)
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
                        data = json.dumps(data)
                        response_data.append(data)
                    return paginator.get_paginated_response(response_data)
                    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
                except:
                    return JsonResponse({'Result': 'No Session exists to Send data'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not authorized to Restart session'}, status=status.HTTP_400_BAD_REQUEST)
 
class last_session_amt(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            try:
                activesession = session.objects.get(isActive=True,location__lname = request.data['location'])
                return JsonResponse({'Result': 'There exits an already active session'}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            except:
                if session.objects.filter(location__lname = request.data['location']).exists():
                    data = session.objects.filter(location__lname = request.data['location'],is_latest=True)
                    sess = data[0]
                    aset = verification.objects.filter(sessionId=sess.sessionId)
                    totalaset = len(aset)
                    founaset = len(verification.objects.filter(sessionId = sess.sessionId).filter(flag = True))
                    amt = 0
                    notfnd = verification.objects.filter(sessionId = sess.sessionId).filter(flag = False)
                    for datas in notfnd:
                        if datas.asset.amount != "":
                            amt = amt + int(datas.asset.amount)
                    return JsonResponse({'TotalAsset':totalaset,'FoundAsset':founaset,'Amount':amt},status = status.HTTP_200_OK)        

                else:
                    return JsonResponse({'Result': 'No Session exists to Send data'}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({'error': 'user is not authorized to Restart session'}, status=status.HTTP_400_BAD_REQUEST)  
 

    
    
