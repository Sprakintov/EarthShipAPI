# Generated by Django 5.1.5 on 2025-02-07 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shipment', '0010_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Shipment.package'),
        ),
    ]
