from django.urls import path
from . import views 
from api import views as Shipmentviews

urlpatterns = [
    #User CRUD endpoints
    path('',views.get_users),
    path('<str:pk>',views.get_user),
    path('addUser/',views.addUser),

    path('referral/create/', views.create_referral, name='create_referral'),
    # path('referral/update/<str:pk>/', views.update_referral, name='update_referral'),
    # path('referral/delete/<str:pk>/', views.delete_referral, name='delete_referral'),


    #Address CRUD endpoints
    # path('addresses/', Shipmentviews.showAddresses),
    # path('addresses/<str:pk>/', Shipmentviews.getAddress),
    # path('addresses/add/', Shipmentviews.addAddress),
    # path('addresses/update/<str:pk>/', Shipmentviews.updateAddress),
    # path('addresses/delete/<str:pk>/', Shipmentviews.deleteAddress),
]


