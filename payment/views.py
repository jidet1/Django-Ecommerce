from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from store.models import Product, Profile
import time
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
import requests
import logging



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


logger = logging.getLogger(__name__)

def billing_info(request):
    if request.method == "POST":
        # Get cart data
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Validate cart
        if not cart_products or totals <= 0:
            logger.error(f"Invalid cart: products={len(cart_products)}, total={totals}")
            messages.error(request, "Your cart is empty or has an invalid total. Please add items.")
            return redirect('cart_summary')

        # Validate shipping form
        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            # Save shipping info
            shipping_info = shipping_form.save()
            
            # Format shipping address
            shipping_address = (
                f"{shipping_info.shipping_full_name}, "
                f"{shipping_info.shipping_address1}, "
                f"{shipping_info.shipping_address2 or ''}, "
                f"{shipping_info.shipping_city}, "
                f"{shipping_info.shipping_state or ''}, "
                f"{shipping_info.shipping_zip_code or ''}, "
                f"{shipping_info.shipping_country}"
            ).replace(", ,", ",").strip(", ")

            # Validate email
            email = shipping_form.cleaned_data.get('shipping_email')
            if not email or not '@' in email:
                logger.error(f"Invalid email: {email}")
                messages.error(request, "Please provide a valid email address.")
                return render(request, 'payment/check_out.html', {
                    'cart_products': cart_products,
                    'quantities': quantities,
                    'totals': totals,
                    'shipping_form': shipping_form
                })

            # Create order
            try:
                tx_ref = "txref-" + str(int(time.time()))
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=shipping_form.cleaned_data.get('shipping_full_name', ''),
                    email=email,
                    shipping_address=shipping_address,
                    amount_paid=float(totals),
                    tx_ref=tx_ref
                )
                logger.debug(f"Created order: id={order.id}, tx_ref={order.tx_ref}, amount_paid={order.amount_paid}, email={order.email}")
                if not order.tx_ref:
                    logger.error(f"Failed to set tx_ref for order: id={order.id}")
                    messages.error(request, "Failed to generate transaction reference. Please try again.")
                    return redirect('home')
                # Create OrderItem entries
                for product, qty in zip(cart_products, quantities.values()):
                    price = float(product.sale_price if product.is_sale else product.price)
                    OrderItem.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        order=order,
                        product=product,
                        quantity=qty,
                        price=price
                    )
                
                # Store order_id in session
                request.session['order_id'] = order.id
                return redirect('payment_page')  # Redirects to /payment/
            except Exception as e:
                logger.error(f"Order creation failed: {str(e)}")
                messages.error(request, "Failed to create order. Please try again.")
                return render(request, 'payment/check_out.html', {
                    'cart_products': cart_products,
                    'quantities': quantities,
                    'totals': totals,
                    'shipping_form': shipping_form
                })
        else:
            logger.debug(f"Form errors: {shipping_form.errors}")
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'payment/check_out.html', {
                'cart_products': cart_products,
                'quantities': quantities,
                'totals': totals,
                'shipping_form': shipping_form
            })
    else:
        messages.error(request, "Access Denied! Please complete the checkout process.")
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





logger = logging.getLogger(__name__)
def payment_page(request):
    order_id = request.session.get('order_id')
    if not order_id:
        logger.error("No order_id in session")
        messages.error(request, "No order found. Please complete the checkout process.")
        return redirect('home')

    try:
        order = Order.objects.get(id=order_id)
        if order.amount_paid <= 0:
            logger.error(f"Invalid order amount: {order.amount_paid}")
            messages.error(request, "Invalid order amount. Please check your cart.")
            return redirect('cart_summary')
        if not order.email or not '@' in order.email:
            logger.error(f"Invalid order email: {order.email}")
            messages.error(request, "Invalid email address. Please provide a valid email.")
            return redirect('home')
        if not order.tx_ref:
            logger.error(f"Missing tx_ref for order: id={order_id}")
            messages.error(request, "Transaction reference is missing. Please try again.")
            return redirect('home')
        
        logger.debug(f"Order data: id={order.id}, amount_paid={order.amount_paid}, email={order.email}, full_name={order.full_name}")
        return render(request, 'payment/payment.html', {  
            'order_total': float(order.amount_paid),
            'customer_email': order.email,
            'customer_name': order.full_name or 'Guest',
            'flutterwave_public_key': settings.FLUTTERWAVE_PUBLIC_KEY,
            'order_tx_ref': order.tx_ref,
        })
    except Order.DoesNotExist:
        logger.error(f"Order not found: order_id={order_id}")
        messages.error(request, "Order does not exist. Please try again.")
        return redirect('home')

def payment_success(request):
    tx_ref = request.GET.get('tx_ref')
    response = requests.get(
        f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={tx_ref}",
        headers={"Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}"}
    )

    if response.status_code == 200 and response.json().get('status') == 'success':
        # Update order
        order = Order.objects.filter(tx_ref=tx_ref).first()
        if order:
            order.shipped = True
            order.date_shipped = timezone.now()
            order.save()

        # Clear session cart
        request.session.pop('session_key', None)
        request.session.modified = True
        Cart(request)  # Reinitialize to ensure clean state

        return redirect('cart_summary')  # force cart page refresh
    else:
        return render(request, 'payment/error.html', {'error': 'Payment verification failed'})
