from django.contrib import admin
from wuming.models import Category, Customer, Product, Order, Banner, Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Banner)
admin.site.register(Profile)
# Compare this snippet from django_tailwind/wuming/urls.py:

# mix profile and user info
class ProfileInLine(admin.StackedInline):
    model = Profile
    
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)