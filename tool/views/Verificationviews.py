from multiprocessing import AuthenticationError
from django.http import HttpResponse, JsonResponse
from ..models.Verificationmodels import verification as Verification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.Assetmodels import asset as Asset
from ..models.Usermodels import User
from django.core import serializers
import json
from rest_framework import status
# API to Create Verirfication


class create_verification(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

 def post(self, request):
        verification = Verification()
        verification.geo_location = request.data['geo_location']
        verification.sessionId = request.data['sessionId']
        verification.date = request.data['date']
        worker = User.objects.get(id=request.data['worker_id'])
        verification.worker_id = worker
        qr = request.data['Qr_id']
        assetdata = Asset.objects.get(Qr_id=qr)
        print(assetdata)
        verification.asset = assetdata
        verification.save()
        verificationByUser = Verification.objects.filter(
            sessionId=request.data['sessionId'], worker_id=request.data['worker_id'])
        verifications = []
        for data in verificationByUser:
            code = data.asset.item_code
            name = data.asset.item_name
            data = serializers.serialize('json', [data,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            data = json.loads(data)
            data['fields']['item_code'] = code
            data['fields']['item_name'] = name
            verifications.append(data)

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
