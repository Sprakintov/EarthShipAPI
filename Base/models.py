from django.db import models
from UserManagement.models import Customer,PaymentMethod,Agent
# Create your models here.
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    orderDate = models.DateTimeField(auto_now_add=True)
    orderType = models.CharField(max_length=50)
    orderStatus = models.CharField(max_length=50)
    coinsUsed = models.DecimalField(max_digits=10, decimal_places=2)
    orderDiscount = models.IntegerField()
    promoCodeUsed = models.DateTimeField(auto_now_add=True)
    estimatedDelivery = models.DateTimeField()
    deliveryDateTime = models.DateTimeField(null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.OrderID} - {self.orderStatus}"


class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    transactionType = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transactionDateTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)


class Package(models.Model):
    packageID = models.AutoField(primary_key=True)
    packageName = models.CharField(max_length=100)
    packageWidth = models.FloatField()
    packageLength = models.FloatField()
    packageHeight = models.FloatField()
    packageWeight = models.FloatField()
    packageStatus = models.CharField(max_length=50)
    packageDetail = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=100)
    itemDescription = models.TextField()
    itemType = models.CharField(max_length=50)
    itemValue = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)

class OrderHistory(models.Model):
    orderHistoryID = models.AutoField(primary_key=True)
    historyStatus = models.CharField(max_length=50)
    historyCreationDateTime = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Ticket(models.Model):
    ticketID = models.AutoField(primary_key=True)
    ticketAgent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    ticketType = models.CharField(max_length=50)
    ticketStatus = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    content = models.TextField()
    commentDateTime = models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length=255)
    fileType = models.CharField(max_length=50)
    fileSize = models.IntegerField()
    # url = models.URLField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)





class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    invoice_creation_date_time = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

class Shipping(models.Model):
    shippingID = models.AutoField(primary_key=True)
    shippingMethod = models.CharField(max_length=50)
    shippingStatus = models.CharField(max_length=50)
    trackingNumber = models.CharField(max_length=100)
    shippingCreationDateTime = models.DateTimeField(auto_now_add=True)
    type_id = models.IntegerField()
    order = models.OneToOneField(Order, on_delete=models.CASCADE)




