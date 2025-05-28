from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'orders/my_orders.html', {'orders': orders})


from django.shortcuts import get_object_or_404

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Optional: Restrict access for non-staff to only their own orders
    if not request.user.is_staff and order.user != request.user:
        return render(request, 'payment/error.html', {'error': 'Unauthorized access.'})

    return render(request, 'orders/order_detail.html', {'order': order})
