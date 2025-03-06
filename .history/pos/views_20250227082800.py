from django.shortcuts import render
from .models import Product, Order, OrderItem

def menu(request):
    products = Product.objects.filter(available=True)
    return render(request, 'pos/menu.html', {'products': products})

def order_summary(request):
    orders = Order.objects.all()
    return render(request, 'pos/orders.html', {'orders': orders})
