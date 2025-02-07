from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from api.serializers import *
from rest_framework.response import Response


# Order views
@api_view(['GET'])
def showOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

    
@api_view(['POST'])
def addOrder(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



