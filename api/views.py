from rest_framework.decorators import api_view
from .models import *
from api.serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .functions import *
from .DBConnection import query
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# @api_view(['GET'])
# def test(request,pk):
#     cursor = connection.cursor()
#     cursor.execute("""SELECT * FROM 'Base_item' bi WHERE bi.'itemID'=%s""",[pk])
#     row = cursor.fetchone()
#     return Response(row)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def getItemConditions(request):
    """Get all available item conditions for items"""
    sql=query("""select "OrderID" from "public"."Base_order";""")
    print(sql)

@api_view(['GET'])
def getOrderDetails(request,pk):
    order = Order.objects.get(OrderID=pk)
    totalValue=0
    for package in order.packages.all():
        for item in package.items.all():
            totalValue += float(item.itemValue)*float(item.itemQuantity)
            print(float(item.itemValue))
    discount = float(totalValue * order.orderDiscount/100)
    finalValue = totalValue - discount - (float(order.coinsUsed)/100)
    return Response({"Total amount" : totalValue, "Coins used": order.coinsUsed, "Discount 10% ": discount, "Final Value": finalValue})





"""Orders management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageOrders(request,pk=None,items=None,packages=None):
     #Get all orders or a specific order
    if request.method=="GET":
        #Get a specific order
        if pk is not None : 
            try:
                order = Order.objects.get(OrderID=pk)
                serializer = GetOrderSerializer(order)
                return Response(serializer.data)
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        #Get all orders
        else:
            orders = Order.objects.all()

            serializer = GetOrderSerializer(orders, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
    #Add a new order
    if request.method=='POST':
        serializer = OrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data['customer'])
        payment = makePayment(serializer)
        if not payment:
            return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            addCoins(request.data['customer'], 100)
            updateOrderHistory(serializer.data['OrderID'],"Order Placed")
            # addTransaction(request.data['customer'], serializer.data['OrderID'], serializer.data['coinsUsed'], "Success", "Order", None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #Update the order
    elif request.method=='PUT':
        try:
            order = Order.objects.get(OrderID=pk)
            serializer = OrderSerializer(instance=order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                updateOrderHistory(serializer.data['OrderID'], serializer.data['orderStatus'])
                return Response(serializer.data)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    #Delete the order    
    elif request.method=='DELETE':
        try:
            order = Order.objects.get(OrderID=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def refundOrder(request,pk,amount):
    order = Order.objects.get(OrderID=pk)
    customer = Customer.objects.get(customer_id=order.customer.customer_id)
    customer.balance += amount
    customer.ESCoins += order.coinsUsed
    order.orderStatus = "Refunded"
    customer.save()
    order.save()
    addTransaction(order.customer, order.OrderID, order.coinsUsed, "Refund", "Order", None)
    updateOrderHistory(order.OrderID, order.orderStatus)
    return Response({"Yes"})


"""Transactions management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageTransactions(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                transaction = Transaction.objects.get(transactionID=pk)
                serializer = TransactionSerializer(transaction)
                return Response(serializer.data)
            except Transaction.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data)
        
    elif request.method=='POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            transaction = Transaction.objects.get(transactionID=pk)
            serializer = TransactionSerializer(instance=transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method=='DELETE':
        
        try:
            transaction = Transaction.objects.get(transactionID=pk)
            transaction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


"""Package management view"""
@api_view(['GET','POST','PUT','DELETE'])
def managePackages(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                package = Package.objects.get(packageID=pk)
                serializer = PackageSerializer(package)
                return Response(serializer.data)
            except Package.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            packages = Package.objects.all()
            serializer = PackageSerializer(packages, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = PackageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            package = Package.objects.get(packageID=pk)
            serializer = PackageSerializer(instance=package, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Package.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            package = Package.objects.get(packageID=pk)
            package.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Package.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""Item management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageItems(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                item = Item.objects.get(itemID=pk)
                serializer = ItemSerializer(item)
                return Response(serializer.data)
            except Item.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            item = Item.objects.get(itemID=pk)
            serializer = ItemSerializer(instance=item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            item = Item.objects.get(itemID=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""OrderHistory management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageOrderHistories(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                history = OrderHistory.objects.filter(order=pk)
                serializer = OrderHistorySerializer(history, many=True)
                return Response(serializer.data)
            except OrderHistory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            histories = OrderHistory.objects.all()
            serializer = OrderHistorySerializer(histories, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = OrderHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            history = OrderHistory.objects.get(orderHistoryID=pk)
            serializer = OrderHistorySerializer(instance=history, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrderHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            history = OrderHistory.objects.get(orderHistoryID=pk)
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderHistory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""Ticket management view"""


@api_view(['GET','POST','PUT','DELETE'])
def manageTickets(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                ticket = Ticket.objects.get(ticketID=pk)
                serializer = TicketSerializer(ticket)
                return Response(serializer.data)
            except Ticket.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tickets = Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            ticket = Ticket.objects.get(ticketID=pk)
            serializer = TicketSerializer(instance=ticket, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            ticket = Ticket.objects.get(ticketID=pk)
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

"""Comment management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageComments(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                comment = Comment.objects.get(commentId=pk)
                serializer = CommentSerializer(comment)
                return Response(serializer.data)
            except Comment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            comments = Comment.objects.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            comment = Comment.objects.get(commentId=pk)
            serializer = CommentSerializer(instance=comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            comment = Comment.objects.get(commentId=pk)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# OpenTicket view
@api_view(['POST'])
def openTicket(request):
    """
    Open a new ticket with optional order reference
    """
    data = request.data.copy()
    
    # Validate that customer exists
    try:
        customer = Customer.objects.get(pk=data.get('customer'))
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # If order_id is provided, validate it exists and belongs to customer
    order_id = data.get('order')
    if order_id:
        try:
            order = Order.objects.get(OrderID=order_id, customer=customer)
            data['order'] = order.OrderID
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found or does not belong to this customer'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    # Create ticket
    serializer = TicketSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""Attachment management view"""
@api_view(['GET','POST','PUT','DELETE'])
def manageAttachments(request,pk=None):
    if request.method=='GET':
        if pk is not None:
            try:
                attachment = Attachment.objects.get(attachment_id=pk)
                serializer = AttachmentSerializer(attachment)
                return Response(serializer.data)
            except Attachment.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            attachments = Attachment.objects.all()
            serializer = AttachmentSerializer(attachments, many=True)
            return Response(serializer.data)
            
    elif request.method=='POST':
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='PUT':
        try:
            attachment = Attachment.objects.get(attachment_id=pk)
            serializer = AttachmentSerializer(instance=attachment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Attachment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
    elif request.method=='DELETE':
        try:
            attachment = Attachment.objects.get(attachment_id=pk)
            attachment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Attachment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET','POST'])
# def addCountry(request):
#     if request.method=='GET':
#         countries = Countries.objects.all()
#         serializer = CountriesSerializer(countries, many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         serializer = CountriesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ManageOrders(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class ManageTickets(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

class ManageComments(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()