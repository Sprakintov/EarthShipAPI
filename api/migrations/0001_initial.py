# Generated by Django 5.1.5 on 2025-03-02 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UserManagement', '0002_countries_address_country'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentID', models.AutoField(primary_key=True, serialize=False)),
                ('paymentAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paymentDateTime', models.DateTimeField(auto_now_add=True)),
                ('paymentStatus', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemID', models.AutoField(primary_key=True, serialize=False)),
                ('itemName', models.CharField(max_length=100)),
                ('itemDescription', models.TextField()),
                ('itemType', models.CharField(max_length=50)),
                ('itemQuantity', models.IntegerField(null=True)),
                ('itemValue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('itemManufacturingCountry', models.CharField(blank=True, max_length=100, null=True)),
                ('itemHSCode', models.CharField(blank=True, max_length=50, null=True)),
                ('itemCondition', models.CharField(choices=[('New', 'New'), ('Used', 'Used'), ('Damaged', 'Damaged'), ('Broken', 'Broken'), ('Repaired', 'Repaired'), ('Refurbished', 'Refurbished'), ('Faulty', 'Faulty'), ('Other', 'Other')], default='New', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('OrderID', models.AutoField(primary_key=True, serialize=False)),
                ('orderDate', models.DateTimeField(auto_now_add=True)),
                ('orderType', models.CharField(max_length=50)),
                ('orderStatus', models.CharField(max_length=50)),
                ('coinsUsed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('orderDiscount', models.IntegerField()),
                ('promoCodeUsed', models.DateTimeField(auto_now_add=True)),
                ('estimatedDelivery', models.DateTimeField()),
                ('deliveryDateTime', models.DateTimeField(null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserManagement.customer')),
                ('shippingAddressFrom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippingAddressFrom', to='UserManagement.address')),
                ('shippingAddressTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shippingAddressTo', to='UserManagement.address')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentId', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('commentDateTime', models.DateTimeField(auto_now=True)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ZellePayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.payment')),
                ('Attachment', models.FileField(upload_to='zelle_payments/')),
            ],
            bases=('api.payment',),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(primary_key=True, serialize=False)),
                ('fileName', models.CharField(max_length=255)),
                ('fileType', models.CharField(max_length=50)),
                ('fileSize', models.IntegerField()),
                ('url', models.URLField(blank=True, null=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.comment')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.item')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoiceID', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_creation_date_time', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('orderHistoryID', models.AutoField(primary_key=True, serialize=False)),
                ('historyStatus', models.CharField(max_length=50)),
                ('historyCreationDateTime', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
            options={
                'verbose_name': 'Order History',
                'verbose_name_plural': 'Order Histories',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('packageID', models.AutoField(primary_key=True, serialize=False)),
                ('packageName', models.CharField(max_length=100)),
                ('packageWidth', models.FloatField()),
                ('packageLength', models.FloatField()),
                ('packageHeight', models.FloatField()),
                ('packageWeight', models.FloatField()),
                ('packageStatus', models.CharField(max_length=50)),
                ('packageDetail', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserManagement.customer')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='api.order')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.package'),
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('shippingID', models.AutoField(primary_key=True, serialize=False)),
                ('shippingMethod', models.CharField(max_length=50)),
                ('shippingStatus', models.CharField(max_length=50)),
                ('trackingNumber', models.CharField(max_length=100)),
                ('shippingCreationDateTime', models.DateTimeField(auto_now_add=True)),
                ('type_id', models.IntegerField()),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticketID', models.AutoField(primary_key=True, serialize=False)),
                ('ticketType', models.CharField(choices=[('General', 'General'), ('Refund', 'Refund'), ('Complaint', 'Complaint'), ('Other', 'Other')], default='General', max_length=50)),
                ('ticketStatus', models.CharField(max_length=50)),
                ('submitted', models.DateTimeField(auto_now=True)),
                ('lastUpdated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserManagement.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('ticketAgent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserManagement.agent')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.ticket'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transactionID', models.AutoField(primary_key=True, serialize=False)),
                ('transactionType', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=50)),
                ('transactionDateTime', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserManagement.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.order')),
                ('paymentMethod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.paymentmethod')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.payment')),
                ('paymentMethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserManagement.paymentmethod')),
            ],
            bases=('api.payment',),
        ),
    ]
