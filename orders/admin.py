
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'email', 'amount_paid', 'shipped', 'date_ordered']
    list_filter = ['shipped', 'date_ordered']
    search_fields = ['full_name', 'email', 'tx_ref']
