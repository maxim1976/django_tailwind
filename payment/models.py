from django.db import models
from django.contrib.auth.models import User
from wuming.models import Product
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import datetime
# Create your models here.


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=200)
    shipping_email = models.EmailField(max_length=200, blank=True, null=True)    
    shipping_address = models.CharField(max_length=200, blank=True, null=True)    
    date_added = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'


# Create a Shipping Adress for each user
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)

#create Order model

class Order(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True) 
    full_nammes = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    shipping_address = models.TextField(max_length=200, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'


# Auto Add the date shipped when the order is marked as shipped
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped = now


#create Order Items model

class OrderItem(models.Model):
    # Foreign Key   
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return f'Order Item - {str(self.id)}'