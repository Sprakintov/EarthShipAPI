from rest_framework import serializers
from Shipment.models import *
from UserManagement.models import *
from Warehouse.models import *
from api.models import *
from django.db import models
from rest_framework import serializers
from .models import *

class ConditionChoicesSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class ItemSer(serializers.Serializer):
    itemID = serializers.IntegerField(read_only = True)
    itemName = serializers.CharField(max_length = 100)


class ItemSerializer(serializers.ModelSerializer):
    # attachement = AttachmentSerializer()
    class Meta:
        model = Item
        fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'first_name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
                }
        }


    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)



class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Ticket
        fields = (
            'ticketID',
            'ticketType',
            'ticketStatus',
            'submitted',
            'lastUpdated',
            'customer',
            'ticketAgent',
            'order',
            'comments'
        )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Package
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        package = Package.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(package=package, **item_data)
        return package
    

    
class GetOrderSerializer(serializers.ModelSerializer):
    packages = serializers.SerializerMethodField()
    def get_packages(self,obj):
        package_list = Package.objects.filter(order = obj.OrderID)
        dict = []
        for package in package_list : 
            dict.append({"packageID":package.packageID})
        return dict
    
    class Meta : 
        model = Order
        fields = (

            'orderDate',
            'orderType',
            'orderStatus',
            'customer',
            'coinsUsed',
            'orderDiscount',
            'promoCodeUsed',
            'shippingAddressFrom',
            'shippingAddressTo',
            'estimatedDelivery',
            'deliveryDateTime',
            'packages',
        )
        

class OrderSerializer(serializers.ModelSerializer):
    class PackageCreateSerializer(serializers.ModelSerializer):
        class ItemsCreateSerializer(serializers.ModelSerializer):
            class Meta:
                model = Item
                exclude = ['itemID','package']

        items = ItemsCreateSerializer(many=True)
        class Meta:
            model = Package
            exclude = ['packageID','order']

    packages = PackageCreateSerializer(many=True)
    
    class Meta:
        model = Order
        fields = (
            'orderType',
            'orderStatus',
            'customer',
            'coinsUsed',
            'orderDiscount',
            'shippingAddressFrom',
            'shippingAddressTo',
            'estimatedDelivery',
            'deliveryDateTime',
            'packages'
        )
        
    

    def create(self, validated_data):
        packages_data = validated_data.pop('packages')
        order = Order.objects.create(**validated_data)
        total_cost = 0
        for package_data in packages_data:
            items_data = package_data.pop('items')
            package = Package.objects.create(order=order, **package_data)
            for item_data in items_data:
                total_cost += float(item_data.get("itemValue", 0)) * float(item_data.get("itemQuantity", 1))
                Item.objects.create(package=package, **item_data)
            
        
        OrderHistory.objects.create(order=order, historyStatus=order.orderStatus)
        Transaction.objects.create(customer=order.customer, order=order, amount=total_cost, status=order.orderStatus,paymentMethod=None)
        return order

class ShipmentOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShipmentOrder
        fields = '__all__'


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = '__all__'

class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class WarehouseOrderSerializer(serializers.ModelSerializer):
    packages = PackageSerializer(many=True,read_only=True)
    class Meta:
        model = WarehouseOrder
        fields = '__all__'

class ShipPackageSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True,read_only=True)
    class Meta:
        model = ShipPackage
        fields = '__all__'

class ShipItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipItem
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True,read_only=True)
    count = serializers.IntegerField()
    totalValue = serializers.FloatField()

