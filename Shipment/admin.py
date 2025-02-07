from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Users)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Agent)  
admin.site.register(PaymentMethod)
admin.site.register(Address)
admin.site.register(Transaction)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Package)
