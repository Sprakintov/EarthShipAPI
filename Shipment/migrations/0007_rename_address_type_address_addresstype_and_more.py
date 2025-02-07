# Generated by Django 5.1.5 on 2025-02-06 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shipment', '0006_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_type',
            new_name='addressType',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='zip_code',
            new_name='zipCode',
        ),
        migrations.DeleteModel(
            name='Agent',
        ),
    ]
