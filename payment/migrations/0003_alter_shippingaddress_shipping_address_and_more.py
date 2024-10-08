# Generated by Django 5.0.6 on 2024-08-14 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_address_shippingaddress_shipping_address_and_more'),
        ('wuming', '0004_profile_old_cart_alter_profile_address_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='shipping_email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_nammes', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('shipping_address', models.TextField(blank=True, max_length=200, null=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wuming.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
