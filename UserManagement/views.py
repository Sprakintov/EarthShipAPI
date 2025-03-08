from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.shortcuts import get_object_or_404
from .models import *
from api.serializers import *
from rest_framework import status,filters
from . import permissions

# # User management views
# @api_view(['GET'])
# def getUsers(request):
#     users = UserProfile.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getUser(request,pk):
#     try:
#         users = UserProfile.objects.get(userID=pk)
#     except UserProfile.DoesNotExist:
#         return Response(status=404)

#     serializer = UserSerializer(users)
#     return Response(serializer.data)

# @api_view(['POST'])
# def addUser(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)

@api_view(['POST'])
def createReferral(request):
    serializer = ReferralSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)






# @api_view(['GET'])
# def showAddresses(request):
#     addresses = Address.objects.all()
#     serializer = AddressSerializer(addresses, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def getAddress(request, pk):
#     try:
#         address = Address.objects.get(addressID=pk)
#     except Address.DoesNotExist:
#         return Response(status=404)
    
#     serializer = AddressSerializer(address)
#     return Response(serializer.data)

# @api_view(['POST'])
# def addAddress(request):
#     serializer = AddressSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['PATCH'])
# def updateAddress(request, pk):
#     try:
#         address = Address.objects.get(addressID=pk)
#     except Address.DoesNotExist:
#         return Response(status=404)
    
#     serializer = AddressSerializer(address, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def deleteAddress(request, pk):
#     try:
#         address = Address.objects.get(addressID=pk)
#     except Address.DoesNotExist:
#         return Response(status=404)
    
#     address.delete()
#     return Response(status=204)



# @api_view(['POST','GET'])
# def managePaymentMethods(request,pk):
#     if request.method=='GET':
#         if pk is not None:
#             try:
#                 paymentMethod = PaymentMethod.objects.filter(customer=pk)
#                 serializer = PaymentMethodSerializer(paymentMethod, many=True)
#                 return Response(serializer.data)
#             except PaymentMethod.DoesNotExist:
#                 return Response(status=status.HTTP_404_NOT_FOUND)
#         else:
#             paymentMethods = PaymentMethod.objects.all()
#             serializer = PaymentMethodSerializer(paymentMethods, many=True)
#             return Response(serializer.data)
        
#     elif request.method == 'POST':
#         serializer = PaymentMethodSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'PUT':
#         try:
#             paymentMethod = PaymentMethod.objects.get(payment_method_id=pk)
#             serializer = PaymentMethodSerializer(instance=paymentMethod, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except PaymentMethod.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#     elif request.method == 'DELETE':
#         try:
#             paymentMethod = PaymentMethod.objects.get(payment_method_id=pk)
#             paymentMethod.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except PaymentMethod.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        


class UserProfileViewSet(ModelViewSet):
    serializer_class = UserSerializer
    lookup_field = "username"
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields=('first_name','email')


class UserLoginApiView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class manageAddress(ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

class ManagePaymentMethods(ViewSet):
    serializer_class = PaymentMethodSerializer
    def list(self, request, user):
        queryset = PaymentMethod.objects.filter(customer=user)
        serializer = PaymentMethodSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, user, pk):
        queryset = PaymentMethod.objects.get(customer=user, payment_method_id=pk)
        serializer = PaymentMethodSerializer(queryset)
        return Response(serializer.data)
    
    def create(self, request, user):
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def update(self, request, user, pk):
        paymentMethod = get_object_or_404(PaymentMethod, customer=user, payment_method_id=pk)
        serializer = PaymentMethodSerializer(paymentMethod, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def partial_update(self, request, user, pk):
        paymentMethod = get_object_or_404(PaymentMethod, customer=user, payment_method_id=pk)
        serializer = PaymentMethodSerializer(paymentMethod, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, user, pk):
        paymentMethod = get_object_or_404(PaymentMethod, customer=user, payment_method_id=pk)
        paymentMethod.delete()
        return Response(status=204)
    

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()