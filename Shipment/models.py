from django.db import models
# from django.contrib.auth.models import AbstractUser
from api.models import Order

# Create your models here.

class ShipmentOrder(Order):
    
    SOID = models.AutoField(primary_key=True)
    warrantyValue = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    GoldenDiscount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    shippingMethod = models.CharField(max_length=50,null=True,blank=True)
    trackingNumber = models.CharField(max_length=50, null=True, blank=True)
    order = models.OneToOneField(Order, related_name='SO_profile', on_delete=models.CASCADE)
    # label = models.ImageField(upload_to='labels/', null=True, blank=True)
    
# class ShipmentPackage(Package):
#     pass


# class ShipmentItem(Item):
#     pass










