from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import Userviews
from .views import Assetviews
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.views.decorators.csrf import csrf_exempt
from .views import Verificationviews
from .views import Sessionviews
urlpatterns = [
    # End point to login (Type : POST,Header: Empty, Data: email,password)
    path('api/login/', obtain_jwt_token, name='login'),
    path('api/login/verify/', verify_jwt_token, name='verify'),
    # End point to Decode Token(Type : Get,Header: Authorization, Data: token)
    path('api/decode/', csrf_exempt(Userviews.DecodeToken.as_view()), name='decode'),
    # End point to Register User(Type : Post,Header: Authorization, Data: email,password)
    path('api/register/', csrf_exempt(Userviews.register.as_view()),
         name='user_regsiter'),
    # End point to add_asset(Type : Post,Header: Authorization, Data: check model format)
    path('api/addAsset/', csrf_exempt(Assetviews.asset_add.as_view()),
         name='asset_creation'),
    # End point to get previous verification data from asset_id(Type : Get,Header: Authorization,Parameter: asset_id, Data: empty)
    path('api/<slug:asset_id>/verifydetails/',
         csrf_exempt(Assetviews.verification_details.as_view()), name='verifi_detail'),
    # End point to get asset data from asset_id(Type : Get,Header: Authorization,Parameter: asset_id, Data: empty)
    path('api/<slug:asset_id>/getasset/',
         csrf_exempt(Assetviews.asset_get.as_view()), name='asset_detail'),
    # End point for full text search on asset data(Type : Get,Header: Authorization, Data: words searched by user)
    path('api/fullSearch/', csrf_exempt(Assetviews.fullTextSearch.as_view()),
         name='full_TextSearch'),
    # End point to tag qr(Type : Post,Header: Authorization, Data: item_code,Qr_id)
    path('api/tagging/', csrf_exempt(Assetviews.tagQr.as_view()),
         name='tag_qr'),
    # End point to create verification(Type : Post,Header: Authorization, Data: geo_location,date_time,worker_id,item_id)
    path('api/verification/',
         csrf_exempt(Verificationviews.create_verification.as_view()), name='verification'),
    # End point to get verification data from qr(Type:Post,Header:Authorization,Data:Qr_id)
    path('api/verificationdetails_qr', csrf_exempt(
        Verificationviews.get_verification_status.as_view()), name='getdetails_fromqr'),
    # End point to get complete asset table(Type:Get,Header:Authorization,Data:Empty)
    path('api/get_all_asset',
         csrf_exempt(Assetviews.get_all_asset.as_view()), name='get_asset'),
    path('api/createsession',
         csrf_exempt(Sessionviews.create_session.as_view()), name='create_session'),
    path('api/endsession',
         csrf_exempt(Sessionviews.end_session.as_view()), name='endSession'),
    path('api/getsession',
         csrf_exempt(Sessionviews.get_active_session.as_view()), name='get_session'),
    path('api/restart_session',
         csrf_exempt(Sessionviews.restart_last_session.as_view()), name='restart_session'),
    path('api/changepassword',
         csrf_exempt(Userviews.change_password.as_view()), name='passchng')
]
