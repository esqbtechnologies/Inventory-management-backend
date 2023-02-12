import json
from django.core import serializers
from requests import request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
import ivnt_mngmnt.settings as set
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..models.Usermodels import User
from rest_framework import status
import jwt
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


# function to decode data from token
class DecodeToken(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        token = request.data['token']
        try:
            payload = jwt.decode(
                jwt=token, key=set.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=payload['email'])
            if not user.is_active:
                user.is_active = True
                user.save()
            print(user)
            data = serializers.serialize('json', [user,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return Response(data, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
