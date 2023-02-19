from django.http import HttpResponse
from ..models.Verificationmodels import verification as Verification
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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
