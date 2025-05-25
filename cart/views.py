from django.shortcuts import render, get_object_or_404 
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
   #Get the cart
   cart = Cart(request)
   cart_products = cart.get_prods 
   quantites = cart.get_quants
   totals = cart.cart_total()
   return render(request, "cart_summary.html", {'cart_products':cart_products, "quantites":quantites, 'totals':totals})

def cart_add(request):
    #Get the cart
    cart = Cart(request)
    #test for post
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        #look up products in database
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        #Save to a session
        cart.add(product=product, quantity=product_qty)

        #Get cart quantity
        cart_quantity = cart.__len__()

        #return response
        #response = JsonResponse({'Product Name:': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, (f"{product.name} has been added to your cart"))
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        #Call the delete method 
        cart.delete(product=product_id)
        #Get cart quantity
        cart_quantity = cart.__len__()
        #return response
        response = JsonResponse({'product': product_id})
        messages.success(request, (f"The selected product has been removed from your cart"))
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #Get stuff
        product_id = int(request.POST.get('product_id'))
        #look up products in database
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        respone = JsonResponse({'qty':product_qty})
        messages.success(request, (f"The selected product has been updated to {product_qty}")) 
        return respone
        #return redirect('cart_summary')
    