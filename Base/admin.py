from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(Transaction)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Package)
