# Generated by Django 5.1.5 on 2025-02-07 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shipment', '0019_remove_attachment_ticket_attachment_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Shipment.customer'),
        ),
    ]
