from django.db import models
import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from zoneinfo import ZoneInfo  # For handling timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Create a profile for each user
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, max_digits=4, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default='', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)
    
    def __str__(self):
        return self.name


def is_shop_open():
    # Get current time in your timezone (adjust 'Asia/Tokyo' to your timezone)
    current_time = datetime.datetime.now(ZoneInfo("Asia/Taipei")).time()
    
    # Define shop hours
    opening_time = datetime.time(5, 30)  # 5:30 AM
    closing_time = datetime.time(10, 0)  # 10:00 AM
    
    return opening_time <= current_time <= closing_time

def validate_shop_hours():
    if not is_shop_open():
        raise ValidationError(
            "Sorry, our online payment service is only available from 5:30 AM to 10:00 AM."
        )


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date = models.DateTimeField(default=datetime.datetime.now)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100, default='', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    def clean(self):
        super().clean()
        if self.status == 'pending':
            validate_shop_hours()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer.name + ' - ' + self.product.name


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/banners/')
    description = models.TextField(default='', null=True, blank=True)
    link = models.CharField(max_length=100, default='', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Banners'