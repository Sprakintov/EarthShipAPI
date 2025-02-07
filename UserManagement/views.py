from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from api.serializers import *

# User management views
@api_view(['GET'])
def get_users(request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request,pk):
    try:
        users = Users.objects.get(userID=pk)
    except Users.DoesNotExist:
        return Response(status=404)

    serializer = UserSerializer(users)
    return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def create_referral(request):
    serializer = ReferralSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




@api_view(['GET'])
def showAddresses(request):
    addresses = Address.objects.all()
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAddress(request, pk):
    try:
        address = Address.objects.get(addressID=pk)
    except Address.DoesNotExist:
        return Response(status=404)
    
    serializer = AddressSerializer(address)
    return Response(serializer.data)

@api_view(['POST'])
def addAddress(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def updateAddress(request, pk):
    try:
        address = Address.objects.get(addressID=pk)
    except Address.DoesNotExist:
        return Response(status=404)
    
    serializer = AddressSerializer(address, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def deleteAddress(request, pk):
    try:
        address = Address.objects.get(addressID=pk)
    except Address.DoesNotExist:
        return Response(status=404)
    
    address.delete()
    return Response(status=204)