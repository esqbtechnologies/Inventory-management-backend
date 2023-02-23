from os import stat
from django.http import HttpResponse, JsonResponse
from requests import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..models.Assetmodels import asset as Asset
import json
from django.core import serializers
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

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
            print(data)
            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Data Does not exist'}, status=status.HTTP_400_BAD_REQUEST)


# API To add data
class asset_add(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        arrOfassets = request.data
        for asset in arrOfassets:
            if Asset.objects.filter(item_code=asset['item_code']).exists():
                continue
            else:
                new_asset = Asset()
                new_asset.item_code = asset['item_code']
                new_asset.item_name = asset['item_name']
                new_asset.asset_cls = asset['asset_cls']
                new_asset.periodcat = asset['periodcat']
                new_asset.Useful_life = asset['Useful_life']
                new_asset.Remain_life = asset['Remain_life']
                new_asset.Warehouse_location = asset['Warehouse_location']
                new_asset.save()
        return HttpResponse('Data Saved')

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

# API for full text search


class fullTextSearch(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    model = Asset

    def get(self, request):
        query = self.request.GET.get("q")
        search_vector = SearchVector("item_code", "item_name", "asset_cls",
                                     "periodcat", "Useful_life", "Remain_life", "Warehouse_location", "Qr_id")
        search_query = SearchQuery(query)
        res = Asset.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by("-rank")
        print(res)
        data = serializers.serialize('json', [res,])
        struct = json.loads(data)
        data = json.dumps(struct[0])

        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


# API for Tagging

class tagQr(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        asset_id = request.data['item_code']
        qr_id = request.data['Qr_id']
        try:
            asset = Asset.objects.get(item_code=asset_id)
            asset.Qr_id = qr_id
            asset.save()
            return JsonResponse({'Response': 'Qr Tagged'}, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'error': 'Data not saved'}, status=status.HTTP_400_BAD_REQUEST)


# API for getting all Asset

class get_all_asset(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        asset_data = Asset.objects.all()
        data = serializers.serialize('json', [asset_data,])
        struct = json.loads(data)
        data = json.dumps(struct[0])
        print(data)
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
