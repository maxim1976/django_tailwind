# Generated by Django 5.0.6 on 2024-08-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_shippingaddress_shipping_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
