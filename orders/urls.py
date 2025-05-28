# store/urls.py or your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('my-orders/', views.my_orders, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]
