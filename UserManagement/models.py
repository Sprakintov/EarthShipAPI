from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    userID= models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=15)
    mailAddress = models.CharField(max_length=100)
    # password = models.CharField(max_length=128)
    username = models.CharField(max_length=100, unique=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    user_creation_date_time = models.DateTimeField(auto_now_add=True)   
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        swappable = 'AUTH_USER_MODEL'

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
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


    
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



class Referral(models.Model):
    referralID = models.AutoField(primary_key=True)
    referralCode = models.CharField(max_length=50)
    referralCreationDateTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)