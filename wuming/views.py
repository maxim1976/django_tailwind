from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from wuming.models import Category, Customer, Product, Order, Banner, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserSignUpForm, UserUpdateForm, ChangePasswordForm, UserInfoForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django import forms
import json
from cart.cart import Cart

# Create your views here.


def update_info(request):   
        if request.user.is_authenticated:
            current_user = Profile.objects.get(user__id=request.user.id)
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            form = UserInfoForm(request.POST or None, instance=current_user)

            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

            if form.is_valid() or shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, 'Your account has been updated.')
                return redirect('index')
            return render(request, 'wuming/update_info.html', {'form': form, 'shipping_form': shipping_form})
        else:
            messages.error(request, 'Please log in to update your information.')
            return redirect('login')
        



def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated. Please log in again.')
                login(request, current_user)
                return redirect('login')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = ChangePasswordForm(request.user)
        return render(request, 'wuming/update_password.html', {'form': form})
    else:
        return redirect('login') 
            
    # if request.method == 'POST':
    #     form = ChangePasswordForm(request.user, request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Your password has been updated. Please log in again.')
    #         return redirect('login')
    # else:        
    #     form = ChangePasswordForm(request.user)
    # return render(request, 'wuming/update_password.html', {'form': form})
        


def update_user(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('index')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'wuming/update_user.html', {'form': form})
        

def category(request, category):
    products = Product.objects.filter(category=category)
    return render(request, 'wuming/category.html', {'products': products})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'wuming/product.html', {'product': product})
    


def index(request):
    products = Product.objects.all()
    banners = Banner.objects.all()
    return render(request, 'wuming/index.html', {'products': products, 'banners': banners})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #Do some shopping cart stuff here

            current_user = Profile.objects.get(user__id=request.user.id)
            #Get their old cart
            saved_cart = current_user.old_cart
            #convert database string to a dictionary
            if saved_cart:
                #convert the string to a dictionary using JSON
                converted_cart = json.loads(saved_cart)
                
                cart = Cart(request)

                for key, value in converted_cart.items():                    
                    cart.db_add(product=key, quantity=value)





            messages.success(request, 'You have been logged in successfully.')
            return redirect('update_info')
        else:
            messages.success(request, 'Invalid credentials.')
            return redirect('login')

    else:
        return render(request, 'wuming/login.html', {})
   


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out.'))
    return redirect('index')


def register_user(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'wuming/register.html', {'form': form})