from django.db import models
from UserManagement.models import *
# Create your models here.
class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    orderDate = models.DateTimeField(auto_now_add=True)
    orderType = models.CharField(max_length=50)
    orderStatus = models.CharField(max_length=50)
    coinsUsed = models.DecimalField(max_digits=10, decimal_places=2)
    orderDiscount = models.IntegerField()
    promoCodeUsed = models.DateTimeField(auto_now_add=True)
    shippingAddressFrom = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='shippingAddressFrom',null=True,blank=True)
    shippingAddressTo = models.ForeignKey(Address,on_delete=models.CASCADE, related_name='shippingAddressTo',null=True,blank=True)
    estimatedDelivery = models.DateTimeField()
    deliveryDateTime = models.DateTimeField(null=True)
    # totalValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.OrderID} - {self.customer}"


class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    transactionType = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    transactionDateTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True)
    
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
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='packages')

class Item(models.Model):
    class Condition(models.TextChoices):
        NEW = 'New'
        USED = 'Used'
        DAMAGED = 'Damaged'
        BROKEN = 'Broken'
        REPAIRED = 'Repaired'
        REFURBISHED = 'Refurbished'
        FAULTY = 'Faulty'
        OTHER = 'Other'

    itemID = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=100)
    itemDescription = models.TextField()
    itemType = models.CharField(max_length=50)
    itemQuantity = models.IntegerField(null=True)
    itemValue = models.DecimalField(max_digits=10, decimal_places=2)
    itemManufacturingCountry = models.CharField(max_length=100,null=True,blank=True)
    itemHSCode = models.CharField(max_length=50,null=True, blank=True)
    itemCondition = models.CharField(max_length=50, choices=Condition.choices, default=Condition.NEW)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='items',null=True,blank=True)

    @property
    def item_subtotal (self):
        return self.itemValue * self.itemQuantity


class OrderHistory(models.Model):
    orderHistoryID = models.AutoField(primary_key=True)
    historyStatus = models.CharField(max_length=50)
    historyCreationDateTime = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True)

    def updateHistory(self, status):
        self.historyStatus = status
        self.save()

    def __str__(self):
        return f"Order {self.order.OrderID} - {self.historyStatus}"

    class Meta : 
        verbose_name_plural = 'Order Histories'
        verbose_name = 'Order History'


class Ticket(models.Model):
    class Types(models.TextChoices):
        GENERAL = 'General'
        REFUND = 'Refund'
        COMPLAINT = 'Complaint'
        OTHER = 'Other'

    ticketID = models.AutoField(primary_key=True)
    ticketAgent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True)
    ticketType = models.CharField(max_length=50, choices=Types.choices, default=Types.GENERAL)
    ticketStatus = models.CharField(max_length=50)
    submitted = models.DateTimeField(auto_now=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

class Comment(models.Model):
    commentId = models.AutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    commentDateTime = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    

class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    fileName = models.CharField(max_length=255)
    fileType = models.CharField(max_length=50)
    fileSize = models.IntegerField()
    url = models.URLField(null=True,blank=True)
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


class Payment (models.Model):
    paymentID = models.AutoField(primary_key=True)
    paymentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentDateTime = models.DateTimeField(auto_now_add=True)
    paymentStatus = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


class CreditCardPayment(Payment):
    paymentMethod = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)


class ZellePayment(Payment):
    Attachment = models.FileField(upload_to='zelle_payments/')




