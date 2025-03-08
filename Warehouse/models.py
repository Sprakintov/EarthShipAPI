from django.db import models
from api.models import Order,Package,Item
# Create your models here.

class WarehouseOrder(Order):
    BFMID = models.AutoField(primary_key=True)
    ServiceCharge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    isPalette = models.BooleanField(default=False)


class ShipPackage(Package):
    SPID = models.AutoField(primary_key=True)
    TrackingNumber = models.CharField(max_length=50, null=True, blank=True)
    siteName = models.CharField(max_length=100,null=True, blank=True)
    siteURL = models.URLField(null=True, blank=True)
    packageNote = models.TextField(null=True, blank=True)
    BFMID = models.ForeignKey(WarehouseOrder, on_delete=models.CASCADE,null=True, blank=True)
    # packageStatus = models.CharField(max_length=50)
    # packageDetail = models.TextField()


    # def get_package_info(self):
    #     return {
    #         'TrackingNumber': self.TrackingNumber,
    #         'siteName': self.siteName,
    #         'siteURL': self.siteURL,
    #         'packageStatus': self.packageStatus,
    #         'packageDetail': self.packageDetail,
    #         'packageNote': self.packageNote
    #     }

class ShipItem(models.Model):
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
    itemCondition = models.CharField(max_length=50,choices=Condition.choices)
    itemStatus = models.CharField(max_length=50)
    itemDetail = models.TextField()
    package = models.ForeignKey(ShipPackage, on_delete=models.CASCADE)
    order = models.ForeignKey(
        WarehouseOrder, 
        on_delete=models.CASCADE,
        related_name='items')