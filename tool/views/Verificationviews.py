from multiprocessing import AuthenticationError
from django.http import HttpResponse, JsonResponse
import ivnt_mngmnt.settings as set
from tool.models.Sessionmodels import session
from ..models.Verificationmodels import verification as Verification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.Assetmodels import asset as Asset
from ..models.Usermodels import User
from django.core import serializers
import jwt
import json
from datetime import date
from rest_framework import status
# API to Create Verirfication


class create_verification(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        
        qr = request.data['Qr_id']
        assetdata = Asset.objects.get(Qr_id=qr)
        if Verification.objects.filter(sessionId = request.data['sessionId']).filter(asset = assetdata).filter(flag = True).exists():
            return JsonResponse({'error':'The assset had been already verified in the current session'},status=status.HTTP_400_BAD_REQUEST)
        else:        
            verification, created = Verification.objects.get_or_create(
                sessionId = request.data['sessionId'],
                asset = assetdata,
                flag = False,
                defaults = {'date':date.today()}
            )
            print(verification.geo_location)
            # verification.geo_location = request.data['geo_location']
            verification.sessionId = request.data['sessionId']
            verification.date = request.data['date']
            worker = User.objects.get(id=request.data['worker_id'])
            verification.worker_id = worker
            verification.geo_location = worker.location.lname
            verification.flag = True            
            verification.asset = assetdata
            verification.save()
            verificationByUser = Verification.objects.filter(
                sessionId=request.data['sessionId'], worker_id=request.data['worker_id'])
            verifications = []
            for data in verificationByUser:
                code = data.asset.item_code
                name = data.asset.item_name
                dumm = serializers.serialize('json', [data,])
                struct = json.loads(dumm)
                dumm = json.dumps(struct[0])
                dumm = json.loads(dumm)
                dumm['fields']['item_code'] = code
                dumm['fields']['item_name'] = name
                dumm['fields']['locationofitem'] = data.asset.Warehouse_location.lname
                verifications.append(dumm)

            return JsonResponse(verifications, safe=False, status=status.HTTP_200_OK)




# API To get verification details from QR IDs


class get_verification_status(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        qr_id = request.data['Qr_id']
        asset_data = Asset.objects.get(Qr_id=qr_id)
        verifydetails = asset_data.verification_set.all()
        detailArray = []
        for details in verifydetails:
            data = serializers.serialize('json', [details,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            detailArray.append(data)
        return JsonResponse(detailArray, safe=False, status=status.HTTP_200_OK)


class session_data(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            session_id = request.data['sessionId']
            response_data = []
            sdata = Verification.objects.filter(sessionId=session_id)
            for sdatas in sdata:
                code = sdatas.asset.item_code
                name = sdatas.asset.item_name
                amt = sdatas.asset.amount
                data = serializers.serialize('json', [sdatas,])
                struct = json.loads(data)
                data = json.dumps(struct[0])
                data = json.loads(data)
                data['fields']['item_code'] = code
                data['fields']['item_name'] = name
                data['fields']['locationofitem'] = sdatas.asset.Warehouse_location.lname
                data['fields']['amount'] = amt
                response_data.append(data)
            return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse({'error': 'user is not authorized to get Data'}, status=status.HTTP_400_BAD_REQUEST)


class add_comment(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            asset = request.data['item_code']
            session_id = request.data['sessionId']
            comme = request.data['comment']
            assetdata = Asset.objects.get(item_code=asset)
            verr = Verification.objects.get(sessionId = session_id,asset = assetdata)
            if verr.flag == True:
                return JsonResponse({'error':'This is a verified asset. Cant add comment'},status = status.HTTP_400_BAD_REQUEST)
            else:
                ver = Verification.objects.get(sessionId=session_id,asset = assetdata)
                print("working")
                ver.sessionId = session_id
                ver.date = date.today()
                ver.comment = comme
                ver.asset = assetdata
                ver.flag = False    
                ver.save()
                return JsonResponse({'Respone':'Comment Added Succesfully'},status = status.HTTP_200_OK)
        return JsonResponse({'error': 'user is not authorized to get Data'}, status=status.HTTP_400_BAD_REQUEST)

    
class get_verification_byuser(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        verificationByUser = Verification.objects.filter(
                sessionId=request.data['sessionId'], worker_id=request.data['worker_id'])
        verifications = []
        for data in verificationByUser:
            code = data.asset.item_code
            name = data.asset.item_name
            dumm = serializers.serialize('json', [data,])
            struct = json.loads(dumm)
            dumm = json.dumps(struct[0])
            dumm = json.loads(dumm)
            dumm['fields']['item_code'] = code
            dumm['fields']['item_name'] = name
            dumm['fields']['locationofitem'] = data.asset.Warehouse_location.lname
            verifications.append(dumm)
        return JsonResponse(verifications, safe=False, status=status.HTTP_200_OK)
