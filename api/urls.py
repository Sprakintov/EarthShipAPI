from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_data),
    path('add/',views.addItem),
    # path('showOrders/',views.showOrders),
    # path('addOrder/',views.addOrder),
  

]
