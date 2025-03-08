from UserManagement.models import Customer
from api.models import Order, OrderHistory
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
import datetime
  

def calculateTotalOrder(serializer):
    ser = OrderSerializer(serializer)
    print(ser)
    itemsValue = 0
    for package in ser.packages.all():
        for item in package.items.all():
            itemsValue += item.itemQuantity
    totalValue = itemsValue 
    return totalValue

def makePayment(order):
    print(order)
    payments= {
        "coins": 1500,
        "wallet": 80,

    }
    customer = Customer.objects.get(customer_id=order.data['customer'])
    if payments.coins:
        customer.ESCoins -= payments.coins
        addTransaction(order.customer, orderID=order.orderID, amount=payments.coins, transactionStatus="Success", transactionType="Payment", paymentMethod="ES Coins")

    if payments.wallet:
        # wallet = Wallet.objects.get(customer=order.customer)
        customer.Balance -= payments.wallet
        addTransaction(order.customer, orderID=order.orderID, amount=payments.wallet, transactionStatus="Success", transactionType="Payment", paymentMethod="Wallet")
    #     addTransaction(order.customer, orderID=order.orderID, amount=payments.wallet, transactionStatus="Success", transactionType="Payment", paymentMethod="Wallet")

    # if payments.creditCard:
    #     addTransaction(order.customer, orderID=order.orderID, amount=payments.creditCard, transactionStatus="Success", transactionType="Payment", paymentMethod="Credit Card")

    # if payments.zelle :
    #     addTransaction(order.customer, orderID=order.orderID, amount=payments, transactionStatus="Success", transactionType="Payment", paymentMethod="Zelle")


    # if 0 < coinsUsed < 500:
    #     return False
    # if customer.ESCoins < coinsUsed:
    #     return False
    # customer.ESCoins -= coinsUsed
    customer.save()
   
    return True

def useWallet(id, amount):
    pass




def addCoins(id, amount):
    customer = Customer.objects.get(customer_id=id)
    customer.ESCoins += amount
    customer.save()
    addTransaction(customerID=id, orderID=None, amount=amount, transactionStatus="Success", transactionType="Add Coins", paymentMethod=None)
    return True

def referral(id):
    customer = Customer.objects.get(customer_id=id)
    if customer.refUser is None:
        return False
    refUser = Customer.objects.get(customer_id=customer.refUser.customer_id)
    refUser.ESCoins += 100
    refUser.save()
    return True


def updateOrderHistory(orderID,orderStatus):
    serializer = OrderHistorySerializer(data={'order':orderID,'historyStatus':orderStatus})
    if serializer.is_valid():
        print(serializer.data)
        serializer.save()
        return True
    return False
    


def addTransaction(customerID, orderID, amount, transactionStatus, transactionType, paymentMethod):
    serializer = TransactionSerializer(data={'customer': customerID, 'paymentMethod': paymentMethod, 'order': orderID, 'amount': amount, 'status': transactionStatus, 'transactionType': transactionType})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
