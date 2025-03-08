from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Package, Item
from UserManagement.models import Customer
from api.serializers import OrderSerializer, PackageSerializer, ItemSerializer,TransactionSerializer
from .functions import *
@api_view(['POST'])
def create_order(request):
    try:
        data = request.data
        customer = Customer.objects.get(customer_id=data.get('customer')) 
        packages = data.get('packages')
        if not packages:
            return Response({"error": "No packages provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_cost = 0
        for package in packages:
            if not package.get("items"):
                return Response({"error": "No items provided for package"}, status=status.HTTP_400_BAD_REQUEST)
            
            for item in package.get("items"):
                total_cost += item.get("itemValue", 0) * item.get("itemQuantity", 1)

        if customer.balance < total_cost:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        order = OrderSerializer(data=request.data)
        if order.is_valid():
            order.save()
            print (order.data)
            customer.balance = (float(customer.balance)) - total_cost
            customer.save()
            # updateOrderHistory(order.data['orderID'], "Order placed")
            # addTransaction(order.validated_data['customer'], orderID=order.validated_data['orderID'], amount=total_cost, transactionStatus="Success", transactionType="Payment", paymentMethod="Wallet")
            return Response(order.data, status=status.HTTP_201_CREATED)
       
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
