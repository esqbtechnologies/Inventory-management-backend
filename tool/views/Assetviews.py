from genericpath import exists
from os import stat
from django.http import HttpResponse, JsonResponse
from requests import Response
import ivnt_mngmnt.settings as set
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.Assetmodels import asset as Asset
from ..serializers import Assetserializer
import json
import jwt
from ..models.Usermodels import User
from ..models.Locationmodels import location
from django.core import serializers
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.pagination import PageNumberPagination

# API To get asset from item_code


class asset_get(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, asset_id):
        if Asset.objects.filter(item_code=asset_id).exists():
            # print("YES")
            asset_data = Asset.objects.get(item_code=asset_id)
            print(asset_data)
            data = serializers.serialize('json', [asset_data,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            data = json.loads(data)
            data['fields']['location'] = asset_data.Warehouse_location.lname
            data = json.dumps(data)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Data Does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class asset_add(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        arrOfassets = request.data
        added_sucesfully = []
        coun = 1
        for asset in arrOfassets:
            if Asset.objects.filter(item_code=asset['itemCode']).exists():
                continue
            else:
                if location.objects.filter(lname = asset['warehouseLocation']).exists():
                    new_asset = Asset()
                    new_asset.item_code = asset['itemCode']
                    new_asset.item_name = asset['itemName']
                    new_asset.asset_cls = asset['assetClass']
                    new_asset.periodcat = asset['periodCat']
                    new_asset.Useful_life = asset['usefulLife']
                    new_asset.Remain_life = asset['remainLife']
                    new_asset.amount = asset['amount']
                    new_asset.Warehouse_location = location.objects.get(lname=asset['warehouseLocation'])
                    new_asset.save()
                    data = serializers.serialize('json', [new_asset,])
                    struct = json.loads(data)
                    data = json.dumps(struct[0])
                    data = json.loads(data)
                    data['fields']['location'] = asset['warehouseLocation']
                    data = json.dumps(data)
                    added_sucesfully.append(data)
                    coun = coun + 1
                else:
                    return JsonResponse({'error':'The location given at line ' + str(coun) + ' does not exists in DB'},status = status.HTTP_406_NOT_ACCEPTABLE)    
        return JsonResponse(added_sucesfully, safe=False, status=status.HTTP_200_OK)

# API to retrive all verifications for asset


class verification_details(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request, asset_id):
        asset_data = Asset.objects.get(item_code=asset_id)
        verifydetails = asset_data.verification_set.all()
        print(verifydetails)
        detailArray = []
        for details in verifydetails:
            data = serializers.serialize('json', [details,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            detailArray.append(data)
        # print(data)
        return JsonResponse(detailArray, safe=False, status=status.HTTP_200_OK)

class MySerializer():
    def __init__(self):
    
    def to_representation(self, instance):
        return serializers.serialize('json', [instance])
    
    
class fullTextSearch(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = MySerializer
    model = Asset
    
    def get_queryset(self):
        query = self.request.query_params.get("q")
        print(query)
        search_vector = SearchVector("item_code", "item_name", "asset_cls",
                                     "periodcat", "Useful_life", "Remain_life", "Warehouse_location", "Qr_id")
        search_query = SearchQuery(query)
        queryset = Asset.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by("-rank")
        print(queryset)
        serialized_data = self.serializer_class.to_representation(queryset)
        print(serialized_data)
#         outpt = []
#         for resul in queryset:
#             data = serializers.serialize('json', [resul,])
#             struct = json.loads(data)
#             data = json.dumps(struct[0])
#             outpt.append(data)
        return JsonResponse(serialized_data, safe=False, status=status.HTTP_200_OK)


# API for Tagging

class tagQr(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        asset_id = request.data['item_code']
        qr_id = request.data['Qr_id']
        if Asset.objects.filter(Qr_id=qr_id).exists():
            return JsonResponse({'Response': 'The Qr is already tagged to an asset'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if Asset.objects.filter(item_code=asset_id).exists():
                print("found")
                asset = Asset.objects.get(item_code=asset_id)
                asset.Qr_id = qr_id
                asset.save()
                return JsonResponse({'Response': 'Qr Tagged'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': 'Data not saved'}, status=status.HTTP_400_BAD_REQUEST)


# API for getting all Asset

# class get_all_asset(APIView):

#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (JSONWebTokenAuthentication,)

#     def get(self, request):
#         asset_data = Asset.objects.all()
#         response_data = []
#         for asset in asset_data:
#             data = serializers.serialize('json', [asset,])
#             struct = json.loads(data)
#             data = json.dumps(struct[0])
#             data = json.loads(data)
#             data['fields']['location'] = asset.Warehouse_location.lname
#             data = json.dumps(data)
#             response_data.append(data)
#         return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

class get_all_asset(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def get(self, request):
        aset = Asset.objects.all()
        page_size = 100
        response_data = []
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        asset_data = paginator.paginate_queryset(aset,request)
        for asset in asset_data:
            data = serializers.serialize('json', [asset,])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            data = json.loads(data)
            data['fields']['location'] = asset.Warehouse_location.lname
            data = json.dumps(data)
            response_data.append(data)
        return paginator.get_paginated_response(response_data)

# API to delete asset

class delete_asset(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self,request):
        token = request.headers['Authorization']
        token = token[4:]
        payload = jwt.decode(jwt=token, key=set.SECRET_KEY,
                             algorithms=['HS256'])
        user = User.objects.get(email=payload['email'])
        if user.role == 'General_manager':
            code = request.data['item_code']
            ass = Asset.objects.get(item_code = code)
            ass.is_deleted = True
            ass.save()
            return JsonResponse({'Response':'Asset Deleted Sucesfully'},status = status.HTTP_200_OK)
        return JsonResponse({'error': 'user is not authorized to delete asset'},status = status.HTTP_400_BAD_REQUEST)
