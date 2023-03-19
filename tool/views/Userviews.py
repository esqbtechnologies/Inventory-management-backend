from ..models.Usermodels import MyUserManager
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from requests import request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.views import ObtainJSONWebToken
from django.shortcuts import render
from ..serializers import DataSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
import ivnt_mngmnt.settings as set
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from ..models.Usermodels import User
from ..models.Otpmodels import otp as OTP
from rest_framework import status
import jwt
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

# function to login user


class obtain_token(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if email is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400
                            )
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        json_data = {"email": email,
                     "password": password}
        token = jwt.encode(payload=json_data, key=set.SECRET_KEY,
                           algorithm='HS256')
        return Response({'token': token},
                        status=status.HTTP_200_OK)

# function to decode data from token


class DecodeToken(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
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


# function to register new user


class register(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        role = "Worker"
        if request.data['role'] == '1':
            role = "General_manager"
        if request.data['role'] == '2':
            role = "Store_manager"
        user = User()
        user.email = email
        user.set_password(password)
        user.role = role
        user.save()
        return HttpResponse('User Created')


class obtainToken(ObtainJSONWebToken):
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        otp = request.data['otp']
        try:
            user = authenticate(email=email, password=password)
            tdata = OTP.objects.get(user_id=user.pk)
            if not user or tdata.num != otp or tdata.flag == True:
                return JsonResponse({'Response': 'otp did not matched'})
            tdata.flag = True
            res = super().post(request)
            return res
        except:
            return JsonResponse({'Response': 'No data found'})


class change_password(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        email = request.data['email']
        Newpassword = request.data['Newpassword']
        otp = request.data['otp']
        try:
            user = User.objects.get(email=email)
            tdata = OTP.objects.get(user_id=user.pk)
            if not user or tdata.num != otp or tdata.flag == True or Newpassword is None:
                return JsonResponse({'Response': 'otp did not matched'})
            tdata.flag = True
            user.set_password(Newpassword)
            user.save()
            return JsonResponse({'Response': 'Password changed succesfully'})
        except:
            return JsonResponse({'Response': 'No data found'})
