from django.db import models
from api.models import Order

# Create your models here.
class BuyForMeOrder(Order):
    BFMID = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order,related_name='BFM_profile',on_delete=models.CASCADE)
    siteName = models.CharField(max_length=100)
    siteURL = models.URLField()
    ServiceCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)