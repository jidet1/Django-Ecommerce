from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

# Register ShippingAddress and OrderItem directly
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend the Order model in the admin
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]
    list_display = ["id", "user", "full_name", "shipped", "date_ordered", "date_shipped"]
    list_filter = ["shipped", "date_ordered"]
    search_fields = ["user__username", "full_name", "email"]

# Register Order with custom admin
admin.site.register(Order, OrderAdmin)
