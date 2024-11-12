from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from wuming.models import Product, Profile, is_shop_open
import datetime
from django.http import HttpResponseForbidden

# Create your views here.


def order_detail(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            # Check if true or false
            if status == 'true':
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the order
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                # Get the order
                order = Order.objects.filter(id=pk)
                # Update the order
                order.update(shipped=False)
            messages.success(request, 'Order status updated successfully!')
            return redirect('index')


        return render(request, 'payment/order_detail.html',{"order": order, "items": items})
    else:
        messages.error(request, 'You are not authorized to view this page!')
        return redirect('index')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            # get the order
            order = Order.objects.filter(id=num)
            # update the order
            now = datetime.datetime.now()
            order.update(shipped=True, date_shipped=now)
           # redirect to the same page
            messages.success(request, 'Order status updated successfully!')
            return redirect('not_shipped_dash')


        return render(request, 'payment/not_shipped_dash.html',{"orders": orders})
    else:
        messages.error(request, 'You are not authorized to view this page!')
        return redirect('index')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            # update the order
            now = datetime.datetime.now()
            order.update(shipped=False)
           # redirect to the same page
            messages.success(request, 'Order status updated successfully!')
            return redirect('index')
        return render(request, 'payment/shipped_dash.html',{"orders": orders})
    else:
        messages.error(request, 'You are not authorized to view this page!')
        return redirect('index')


def process_order(request):
    if request.POST:
        # Get the Cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # get  billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        # get shipping session data
        my_shipping = request.session.get('my_shipping')

        # gather order info
        full_names = my_shipping['shipping_full_name']
        phone = my_shipping['shipping_phone']
        email = my_shipping['shipping_email']
        # Create Shipping Address from the session data
        shipping_address = f"{my_shipping['shipping_full_name']}, {my_shipping['shipping_phone']}, {my_shipping['shipping_email']}, {my_shipping['shipping_address']}"
        amount_paid = totals

        # Create the Order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_nammes=full_names, phone=phone, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()


            # Create Order Items
            # get the order ID
            order_id = create_order.pk
            # get products in the cart
            for product in cart_products():
                product_id = product.id
                # get price of the product
                price = product.price
                # get the quantity of the product
                for key,value in quantities().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(product_id=product_id, order_id=order_id, user=user, quantity=value, price=price)
                        create_order_item.save()

            # Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            # Delete Cart from Database(old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete the cart
            current_user.update(old_cart="")

            messages.success(request, 'Your order has been placed successfully!')
            return redirect('index')

        else:
            create_order = Order(full_nammes=full_names, phone=phone, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()


            # get the order ID
            order_id = create_order.pk
            # get products in the cart
            for product in cart_products():
                product_id = product.id
                # get price of the product
                price = product.price

                # get the quantity of the product
                for key,value in quantities().items():
                    if int(key) == product_id:
                        # create order item
                        create_order_item = OrderItem(product_id=product_id, order_id=order_id, quantity=value, price=price)
                        create_order_item.save()


            # Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the session key
                    del request.session[key]        



            messages.success(request, 'Your order has been placed successfully!')
            return redirect('index')

    else:
        messages.error(request, 'There was an error processing your order!')
        return redirect('index')


def billing_info(request):
    # Check if the form is submitted
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session for the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Get the user logged in
        if request.user.is_authenticated:
            #Get the Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})
        else:
            # Checked out as guest
            #Get the Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',{"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form": billing_form})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html',{"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        return redirect('index')


def payment_success(request):
    return render(request, 'payment/payment_success.html',{})

def checkout(request):

    if not is_shop_open():
        return HttpResponseForbidden(
            "Sorry, our online payment service is only available from 5:30 AM to 10:00 AM."
        )

    else:

        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        if request.user.is_authenticated:
            # Get the user logged in
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            return render(request, 'payment/checkout.html',{"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
        else:
            # Checked out as guest
            shipping_form = ShippingForm(request.POST or None)
            return render(request, 'payment/checkout.html',{"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})    