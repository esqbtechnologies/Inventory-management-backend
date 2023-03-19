from ..models.Otpmodels import otp
from ..models.Usermodels import User
from errno import errorcode
from django.contrib.auth import authenticate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework_jwt.settings import api_settings
from datetime import datetime
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import jwt
import random
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


class otpRequest(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            if not user:
                return JsonResponse({'Response': 'No user found with this Email'})
            token1 = random.randint(1000, 9999)
            data = otp()
            data.num = token1
            data.user_id = user
            data.date = datetime.now()
            data.save()
            subject = 'welcome to Esqb Inventory Management system'
            message = f'Hi {user.email}, thank you for Using the Service.The otp to login/Change Password is {token1}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return JsonResponse({'Response': 'Check Your Email For the OTP'})
        except:
            return JsonResponse({'Response': 'No User found with this'})
