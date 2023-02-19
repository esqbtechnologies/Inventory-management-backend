from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import Userviews
from .views import Assetviews
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/login/', obtain_jwt_token, name='login'),
    path('api/login/verify/', verify_jwt_token, name='verify'),
    path('api/decode/', csrf_exempt(Userviews.DecodeToken.as_view()), name='decode'),
    path('api/register/', csrf_exempt(Userviews.register.as_view()),
         name='user_regsiter'),
    path('api/addAsset/', csrf_exempt(Assetviews.asset_add.as_view()),
         name='asset_creation'),
    path('api/<slug:asset_id>/verifydetails/',
         csrf_exempt(Assetviews.verification_details.as_view()), name='verifi_detail'),
    path('api/<slug:asset_id>/getasset/',
         csrf_exempt(Assetviews.asset_get.as_view()), name='asset_detail'),
    path('api/fullSearch/', csrf_exempt(Assetviews.fullTextSearch.as_view()),
         name='full_TextSearch'),
    path('api/tagging/', csrf_exempt(Assetviews.tagQr.as_view()),
         name='tag_qr'),
]
