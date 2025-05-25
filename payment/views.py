from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from store.models import Product, Profile
import datetime

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the order by primary key
        try:
            order = Order.objects.get(id=pk)
            order_items = OrderItem.objects.filter(order=pk)

            if request.POST:
                status = request.POST['shipping_status']
                #Check if True or False
                if status == "True":
                    order = Order.objects.filter(id=pk)
                    #Update Status
                    now = datetime.datetime.now()
                    order.update(shipped=True, date_shipped = now)
                    messages.success(request, "Order Status Updated Successfully!")
                    return redirect('home') 
                else:
                    order = Order.objects.filter(id=pk)
                    #Update Status
                    order.update(shipped=False)

                    messages.success(request, "Order Status Updated Successfully!")
                    return redirect('home') 
                
                
            return render(request, "payment/orders.html", {
                'order': order,
                'order_items': order_items,
            })
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
            return redirect('home')
        return render(request, "payment/orders.html", {})
    else:
        messages.error(request, "Access Denied! You do not have permission to view this page.")
        return redirect('home')


from django.shortcuts import get_object_or_404
from django.contrib import messages
import datetime
from .models import Order

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)

        if request.method == 'POST':
            status = request.POST.get('shipping_status')
            num = request.POST.get('num')

            # Only update the order with this specific ID
            order = get_object_or_404(Order, id=num)

            now = datetime.datetime.now()

            if status == "True":
                order.shipped = True
                order.date_shipped = now
                order.save()
                messages.success(request, "Order marked as shipped.")
            else:
                order.shipped = False
                order.save()
                messages.success(request, "Order marked as not shipped.")

            return redirect('not_shipped_dash')

        return render(request, "payment/not_shipped_dash.html", {
            'orders': orders,
        })

    else:
        messages.error(request, "Access Denied! You do not have permission to view this page.")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)

        if request.method == 'POST':
            status = request.POST.get('shipping_status')
            num = request.POST.get('num')

            # Get the specific order by ID
            order = get_object_or_404(Order, id=num)

            # Update the order
            order.shipped = False
            order.date_shipped = None  # Optional: clear shipped date
            order.save()

            messages.success(request, "Order Status Updated Successfully!")
            return redirect('shipped_dash')  # redirect to the same page

        return render(request, "payment/shipped_dash.html", {
            'orders': orders,
        })

    else:
        messages.error(request, "Access Denied! You do not have permission to view this page.")
        return redirect('home')

def process_order(request):
    if request.POST:
        #Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantites = cart.get_quants
        totals = cart.cart_total()

        #Get billing info from the form
        payment_form = PaymentForm(request.POST or None) 
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        
        #Create my shipping address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}\n{my_shipping['shipping_zip_code']}"
        amount_paid = totals

        #Create an order 
        if request.user.is_authenticated:
            #logged in
            user= request.user
            #Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()


            #Add order items to the order
            #Get order id
            order_id = create_order.pk
            #Get product info
            for product in cart_products():
                profuct_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #Get product quantity
                for key, value in quantites().items():
                    if int(key) == product.id:
                        quantity = value
                        #Create order item
                        create_order_item = OrderItem(user=user, order_id=order_id, product_id=product.id, quantity=quantity, price=price)
                        create_order_item.save()

            #Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            #Clear cart from database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            #Delete cart database
            current_user.update(old_cart="")



            messages.success(request, "Order Placed Successfully!")
            return redirect('home')

        
        else: 
            #not logged in 
            #Create Order
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()


              #Add order items to the order
            #Get order id
            order_id = create_order.pk
            #Get product info
            for product in cart_products():
                profuct_id = product.id
                #Get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                #Get product quantity
                for key, value in quantites().items():
                    if int(key) == product.id:
                        quantity = value
                        #Create order item
                        create_order_item = OrderItem(order_id=order_id, product_id=product.id, quantity=quantity, price=price)
                        create_order_item.save() 
            #Clear the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.success(request, "Order Placed Successfully!")
            return redirect('home')

     

    else:
        messages.error(request, "Access Denied! Please login to continue or register if you do not have an account.")
        return redirect('home')

def billing_info(request):
    if request.method == "POST":
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods 
        quantites = cart.get_quants
        totals = cart.cart_total()

        #Create a session for the shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check if the user is authenticated
        if request.user.is_authenticated:
            #Get billing info from the form
            billing_form = PaymentForm()

            return render(request, "payment/billing_info.html", {
            'cart_products': cart_products,
            'quantites': quantites,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form,
            })
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {
            'cart_products': cart_products,
            'quantites': quantites,
            'totals': totals,
            'shipping_info': request.POST,
            'billing_form': billing_form,
            })

        shipping_form = request.POST 
        return render(request, "payment/billing_info.html", {
            'cart_products': cart_products,
            'quantites': quantites,
            'totals': totals,
            'shipping_form': shipping_form
            })
    else:
        messages.error(request, "Access Denied! Please login to continue or register if you do not have an account.")
        return redirect('home')

def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods 
    quantites = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ObjectDoesNotExist:
            shipping_user = None

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)  # Don't use instance for guest

    return render(request, "payment/checkout.html", {
        'cart_products': cart_products,
        'quantites': quantites,
        'totals': totals,
        'shipping_form': shipping_form
    })

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})
