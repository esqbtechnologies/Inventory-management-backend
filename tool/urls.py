from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import Userviews
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/login/', obtain_jwt_token, name='login'),
    path('api/login/verify/', verify_jwt_token, name='verify'),
    path('api/decode/', csrf_exempt(Userviews.DecodeToken.as_view()), name='decode'),
]
