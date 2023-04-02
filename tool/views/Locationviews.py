from ..models.Locationmodels import location
from rest_framework.views import APIView
from ..models.Usermodels import User
from django.http import JsonResponse
from rest_framework import status
import json
import jwt
import ivnt_mngmnt.settings as set
from django.core import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class addLocation(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'Super_admin':
            loc = request.data['location']
            if location.objects.filter(lname = loc).exists():
                return JsonResponse({'error':'Location already exists'},status = status.HTTP_400_BAD_REQUEST)
            newloc = location()
            newloc.lname = loc
            newloc.save()
            return JsonResponse({'Response':'Location succesfully created'},status = status.HTTP_200_OK)    
        return JsonResponse({'error':'Not Authorized to add location'},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)    

class get_location(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(request,self):
        location_data = location.objects.all()
        response_data = []
        for locations in location_data:
            data = serializers.serialize('json', [locations,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            response_data.append(data)
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

