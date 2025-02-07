# Generated by Django 5.1.5 on 2025-02-07 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shipment', '0009_delete_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itemID', models.AutoField(primary_key=True, serialize=False)),
                ('itemName', models.CharField(max_length=100)),
                ('itemDescription', models.TextField()),
                ('itemType', models.CharField(max_length=50)),
                ('itemValue', models.DecimalField(decimal_places=2, max_digits=10)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shipment.package')),
            ],
        ),
    ]
