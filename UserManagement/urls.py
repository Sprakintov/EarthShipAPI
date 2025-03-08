from django.urls import path
from django.urls import include
from .views import *   
from rest_framework.routers import DefaultRouter


users_router = DefaultRouter()
users_router.register('', UserProfileViewSet)
users_router.register('customer', CustomerViewSet)

user_router = DefaultRouter()
user_router.register('paymentmethods', ManagePaymentMethods, basename='payment-methods')
user_router.register('address', manageAddress)

urlpatterns = [
    #User CRUD endpoints
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('', include(users_router.urls)),
    path('<int:user>/', include(user_router.urls)),
    path('referral/create/', createReferral, name='create_referral'),


    # path('',getUsers),
    # path('<str:pk>',getUser),
    # path('addUser/',addUser),
    # path('referral/update/<str:pk>/', update_referral, name='update_referral'),
    # path('referral/delete/<str:pk>/', delete_referral, name='delete_referral'),


    #Address CRUD endpoints


    # path('addresses/', showAddresses),
    # path('addresses/<str:pk>/', getAddress),
    # path('addresses/add/', addAddress),
    # path('addresses/update/<str:pk>/', updateAddress),
    # path('addresses/delete/<str:pk>/', deleteAddress),
]


