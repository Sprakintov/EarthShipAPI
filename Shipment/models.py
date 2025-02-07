from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

# class Item(models.Model):
#     name = models.CharField(max_length=100)
#     created = models.DateTimeField(auto_now_add=True)
    

class Users(models.Model):
    userID= models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=15)
    mailAddress = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    user_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_creation_date_time = models.DateTimeField(auto_now_add=True)   
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Agent(Users):
    agent_id = models.AutoField(primary_key=True)
    agent_status = models.CharField(max_length=50)
    agent_creation_date_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

  
class Customer(Users):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='customer_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    ESCoins = models.IntegerField(default=500)
    ref_date = models.DateTimeField(auto_now_add=True)

class PaymentMethod(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    card_holder_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)
    expiry = models.DateField()


class Address(models.Model):
    addressID = models.AutoField(primary_key=True)
    addressLine1 = models.CharField(max_length=255)
    addressLine2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    addressType = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')


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
    customer = models.ForeignKey(Users, on_delete=models.CASCADE)

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
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

class OrderHistory(models.Model):
    orderHistoryID = models.AutoField(primary_key=True)
    historyStatus = models.CharField(max_length=50)
    historyCreationDateTime = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

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


class Referral(models.Model):
    referralID = models.AutoField(primary_key=True)
    referralCode = models.CharField(max_length=50)
    referralCreationDateTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)