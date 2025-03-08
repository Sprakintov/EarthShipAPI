from django.contrib import admin
from .models import *
admin.site.site_header = 'EarthShip Admin Dashboard'
admin.site.site_title = 'EarthShip Admin Dashboard'
admin.site.index_title = 'EarthShip Admin Dashboard'
# Register your models here.
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Package)
admin.site.register(OrderHistory)
admin.site.register(Countries)