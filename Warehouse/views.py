from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Warehouse.models import *
from api.serializers import WarehouseOrderSerializer, ShipPackageSerializer,ItemSerializer
from api.functions import *
# Create your views here.


@api_view('GET')
def getWarehouseOrders(request):
    pass