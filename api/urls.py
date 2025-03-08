from django.urls import path, include
from . import views, order_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView



router = DefaultRouter()
router.register('orders', views.ManageOrders, basename='orders')
router.register('tickets', views.ManageTickets, basename='tickets')
router.register('comments', views.ManageComments, basename='comments')

urlpatterns = [
    path('makeorder/', order_views.create_order),
    path('test/', include(router.urls)),  # Test endpoint
    path('<int:pk>',views.getOrderDetails),
    # Order URLs
    path('orders/', views.manageOrders),
    path('orders/<int:pk>/', views.manageOrders),
    path('orders/<int:pk>/refund/', views.refundOrder),
    

    # Transaction URLs
    path('transactions/', views.manageTransactions),
    path('transactions/<int:pk>/', views.manageTransactions),


    # Package URLs
    path('packages/', views.managePackages),
    path('packages/<int:pk>/', views.managePackages),

    # Item URLs
    path('items/', views.manageItems),
    path('items/<int:pk>/', views.manageItems),

    # OrderHistory URLs
    path('order-histories/', views.manageOrderHistories),
    path('order-histories/<int:pk>/', views.manageOrderHistories),

    # Ticket URLs
    path('tickets/', views.manageTickets),
    path('tickets/<int:pk>/', views.manageTickets),
    path('tickets/open/', views.openTicket),  # Keep special openTicket endpoint

    # Comment URLs
    path('comments/', views.manageComments),
    path('comments/<int:pk>/', views.manageComments),

    # Attachment URLs
    path('attachments/', views.manageAttachments),
    path('attachments/<int:pk>/', views.manageAttachments),

    # Countries URLs
    # path('countries/', views.addCountry),


    
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
