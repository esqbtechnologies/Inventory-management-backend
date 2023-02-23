from multiprocessing import AuthenticationError
from django.http import HttpResponse, JsonResponse
from yaml import serialize
from ..models.Verificationmodels import verification as Verification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.Assetmodels import asset as Asset
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
        verification.date_time = request.data['date_time']
        verification.worker_id = request.data['worker_id']
        verification.asset = request.data['item_id']
        verification.save()
        return HttpResponse('verification done')

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
