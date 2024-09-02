from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem inline

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_added"]
    fields = ["user", "full_nammes", "phone", "email", "shipping_address", "amount_paid", "date_added", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

#Unregister the Order model
admin.site.unregister(Order)

# Register the Order model with the OrderAdmin
admin.site.register(Order, OrderAdmin)