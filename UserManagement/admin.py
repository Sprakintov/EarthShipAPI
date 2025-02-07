from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Agent) 
admin.site.register(Users)
admin.site.register(Referral)
admin.site.register(PaymentMethod)
admin.site.register(Address)